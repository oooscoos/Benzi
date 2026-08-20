"""StallionSwipe -- Tinder for horses. Matching engine + demo herd.

A "match" happens when two horses have each swiped right on each other.
The engine scores compatibility (so the deck leads with the best fits),
honours each horse's dealbreakers/filters, tracks passes so they don't
resurface, keeps per-match chat threads, and can serialize the whole
world to a dict for persistence.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple
import time


# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------

@dataclass
class Preferences:
    """What a horse is looking for -- used to filter the deck."""
    genders: Set[str] = field(default_factory=lambda: {"mare", "stallion", "gelding"})
    min_age: int = 0
    max_age: int = 40
    max_distance_km: int = 500
    breeds: Optional[Set[str]] = None          # None = any breed
    must_share_discipline: bool = False        # dealbreaker: no shared hobby, no show


@dataclass
class Horse:
    id: int
    name: str
    breed: str
    age: int                      # years
    gender: str                   # "mare" | "stallion" | "gelding"
    temperament: str              # "chill" | "spirited" | "playful" | "stoic"
    disciplines: List[str]        # e.g. ["dressage", "trail"]
    bio: str
    height_hands: float           # horse height, measured in hands
    photo: str = "\U0001F434"     # emoji fallback for a profile pic
    coat: str = "#8a5a34"         # body colour (drives the SVG portrait in the web app)
    mane: str = "#3d2513"         # mane/tail colour
    marking: str = "none"         # face marking: none|blaze|star|snip|spots
    stable: str = "Meadowbrook"   # location / barn name
    distance_km: int = 0          # distance from the viewer
    verified: bool = False        # blue-hoofmark
    prefs: Preferences = field(default_factory=Preferences)

    likes: Set[int] = field(default_factory=set)     # swiped right on
    passes: Set[int] = field(default_factory=set)    # swiped left on


@dataclass
class Message:
    from_id: int
    text: str
    ts: float = field(default_factory=time.time)


# ----------------------------------------------------------------------------
# Scoring
# ----------------------------------------------------------------------------

def _temperament_bonus(a: "Horse", b: "Horse") -> int:
    good_pairs = {("chill", "spirited"), ("playful", "playful"),
                  ("stoic", "chill"), ("spirited", "spirited"),
                  ("playful", "chill"), ("stoic", "stoic")}
    pair = (a.temperament, b.temperament)
    if pair in good_pairs or pair[::-1] in good_pairs or a.temperament == b.temperament:
        return 10
    return 0


def compatibility(a: "Horse", b: "Horse") -> int:
    """0-100 score. Higher = better hay-day potential."""
    score = 42

    # shared hobbies are the biggest driver
    shared = set(a.disciplines) & set(b.disciplines)
    score += 12 * len(shared)

    score += _temperament_bonus(a, b)

    # similar age (within 4 years) -- nobody likes a big generation gap
    if abs(a.age - b.age) <= 4:
        score += 8

    # similar height (within 2 hands) so nuzzling actually works
    if abs(a.height_hands - b.height_hands) <= 2:
        score += 6

    # same stable -- easy logistics, you already share a paddock
    if a.stable == b.stable:
        score += 5

    # proximity: closer is better, taper off with distance
    if b.distance_km <= 10:
        score += 6
    elif b.distance_km <= 50:
        score += 3

    # verified profiles get a small trust nudge
    if b.verified:
        score += 4

    # geldings are looking for friendship; still fine, just capped enthusiasm
    if "gelding" in (a.gender, b.gender):
        score = min(score, 82)

    return max(0, min(100, score))


def passes_filters(viewer: "Horse", other: "Horse") -> bool:
    """Does `other` satisfy `viewer`'s hard preferences?"""
    p = viewer.prefs
    if other.gender not in p.genders:
        return False
    if not (p.min_age <= other.age <= p.max_age):
        return False
    if other.distance_km > p.max_distance_km:
        return False
    if p.breeds is not None and other.breed not in p.breeds:
        return False
    if p.must_share_discipline and not (set(viewer.disciplines) & set(other.disciplines)):
        return False
    return True


# ----------------------------------------------------------------------------
# Engine
# ----------------------------------------------------------------------------

class StallionSwipe:
    def __init__(self, herd: List[Horse]):
        self.herd: Dict[int, Horse] = {h.id: h for h in herd}
        # chat threads keyed by the sorted (a,b) pair
        self.threads: Dict[Tuple[int, int], List[Message]] = {}

    # -- swiping ------------------------------------------------------------

    def swipe(self, from_id: int, to_id: int, liked: bool) -> bool:
        """Record a swipe. Returns True if this swipe created a mutual match."""
        if from_id not in self.herd or to_id not in self.herd:
            raise ValueError(f"unknown horse in swipe {from_id}->{to_id}")
        me = self.herd[from_id]
        if liked:
            me.passes.discard(to_id)
            me.likes.add(to_id)
            return self.is_match(from_id, to_id)
        me.likes.discard(to_id)
        me.passes.add(to_id)
        return False

    def is_match(self, a_id: int, b_id: int) -> bool:
        return (b_id in self.herd[a_id].likes
                and a_id in self.herd[b_id].likes)

    def matches_for(self, horse_id: int) -> List["Horse"]:
        me = self.herd[horse_id]
        out = [self.herd[o] for o in me.likes if self.is_match(horse_id, o)]
        out.sort(key=lambda h: compatibility(me, h), reverse=True)
        return out

    def deck_for(self, horse_id: int) -> List[Tuple["Horse", int]]:
        """The stack of cards to show `horse_id`, best-match-first.

        Excludes self, anyone already swiped on (either way), and anyone
        who fails the viewer's hard filters.
        """
        me = self.herd[horse_id]
        seen = me.likes | me.passes | {horse_id}
        candidates = [h for h in self.herd.values()
                      if h.id not in seen and passes_filters(me, h)]
        scored = [(h, compatibility(me, h)) for h in candidates]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored

    def undo_last_pass(self, horse_id: int, to_id: int) -> None:
        """Rewind (the 'oops' button)."""
        self.herd[horse_id].passes.discard(to_id)

    # -- chat ---------------------------------------------------------------

    def _key(self, a_id: int, b_id: int) -> Tuple[int, int]:
        return (a_id, b_id) if a_id < b_id else (b_id, a_id)

    def send_message(self, from_id: int, to_id: int, text: str) -> Message:
        if not self.is_match(from_id, to_id):
            raise ValueError("can't message a horse you haven't matched with")
        msg = Message(from_id=from_id, text=text)
        self.threads.setdefault(self._key(from_id, to_id), []).append(msg)
        return msg

    def thread(self, a_id: int, b_id: int) -> List[Message]:
        return self.threads.get(self._key(a_id, b_id), [])

    # -- persistence --------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "herd": [asdict(h) for h in self.herd.values()],
            "threads": {f"{a}-{b}": [asdict(m) for m in msgs]
                        for (a, b), msgs in self.threads.items()},
        }


# ----------------------------------------------------------------------------
# Demo data
# ----------------------------------------------------------------------------

def demo_herd() -> List[Horse]:
    """20 horses: 10 mares + 10 stallions/geldings. Mirrors HERD in index.html."""
    H = Horse
    return [
        # ---- mares (10) ----
        H(1, "Bella", "Arabian", 5, "mare", "playful", ["dressage", "trail"],
          "Desert princess seeking a trail buddy. Must love apples.", 14.3,
          coat="#c9915e", mane="#4a2f1a", marking="blaze", stable="Meadowbrook", distance_km=3, verified=True),
        H(2, "Willow", "Appaloosa", 4, "mare", "spirited", ["barrel", "racing"],
          "Spotted and speedy. Swipe right if you can keep up.", 15.0,
          coat="#d8d2c6", mane="#6b5b4a", marking="spots", stable="Meadowbrook", distance_km=3, verified=True),
        H(3, "Daisy", "Shetland Pony", 9, "mare", "playful", ["shows", "trail"],
          "Small but mighty. Great personality, height is just a number.", 10.1,
          coat="#e8c37a", mane="#7a5a2a", marking="star", stable="Meadowbrook", distance_km=3),
        H(4, "Luna", "Friesian", 5, "mare", "chill", ["dressage", "driving"],
          "All black, all heart. Long mane, longer walks at sunset.", 16.1,
          coat="#2b2b30", mane="#0f0f12", marking="none", stable="Churchill Barn", distance_km=8, verified=True),
        H(5, "Rosie", "Haflinger", 6, "mare", "playful", ["trail", "shows"],
          "Golden girl with a flaxen mane. Sunshine in horse form.", 14.0,
          coat="#d68a3c", mane="#f0e2c0", marking="blaze", stable="Meadowbrook", distance_km=5, verified=True),
        H(6, "Pepper", "Percheron", 7, "mare", "chill", ["driving", "trail"],
          "Dapple-grey and drama-free. Looking for someone to share hay with.", 16.3,
          coat="#9a9aa0", mane="#5a5a60", marking="snip", stable="Highland Stables", distance_km=18),
        H(7, "Ginger", "Morgan", 5, "mare", "spirited", ["dressage", "jumping"],
          "Fiery chestnut with a competitive streak. Bring your A-game.", 15.1,
          coat="#b45f2e", mane="#7a3a18", marking="star", stable="Churchill Barn", distance_km=11, verified=True),
        H(8, "Misty", "Connemara", 8, "mare", "chill", ["jumping", "trail"],
          "Silver-grey and serene. Foggy mornings are my aesthetic.", 14.2,
          coat="#bfc4cc", mane="#7d838c", marking="none", stable="Seaside Paddock", distance_km=31),
        H(9, "Clover", "Welsh Pony", 4, "mare", "playful", ["shows", "barrel"],
          "Lucky in hooves, hopeful in love. Four-leaf energy only.", 12.2,
          coat="#7a5230", mane="#3d2817", marking="snip", stable="Meadowbrook", distance_km=3),
        H(10, "Aurora", "Akhal-Teke", 6, "mare", "stoic", ["dressage", "racing"],
          "Metallic sheen, mysterious vibe. Rare breed, rarer heart.", 15.2,
          coat="#c9a24b", mane="#8a6a2a", marking="blaze", stable="Highland Stables", distance_km=22, verified=True),

        # ---- stallions & geldings (10) ----
        H(11, "Seabiscuit", "Thoroughbred", 6, "stallion", "spirited", ["racing", "trail"],
          "Fast on the track, faster to your heart. Hay is my love language.", 15.2,
          coat="#8a5a34", mane="#3d2513", marking="star", stable="Churchill Barn", distance_km=8, verified=True),
        H(12, "Duke", "Clydesdale", 8, "gelding", "chill", ["driving", "shows"],
          "Big guy, bigger heart. Gentle giant vibes only.", 18.0,
          coat="#5a3a24", mane="#2a1a10", marking="blaze", stable="Highland Stables", distance_km=22),
        H(13, "Comet", "Mustang", 7, "stallion", "spirited", ["trail", "racing"],
          "Wild at heart, free to a good pasture. No fences on my feelings.", 14.2,
          coat="#7d5b3a", mane="#4a3520", marking="snip", stable="Open Range", distance_km=45),
        H(14, "Apollo", "Andalusian", 6, "stallion", "stoic", ["dressage", "shows"],
          "Classically trained, effortlessly elegant. Seeking my dance partner.", 16.0,
          coat="#e6e6ea", mane="#c4c4cc", marking="none", stable="Highland Stables", distance_km=22, verified=True),
        H(15, "Rocky", "Quarter Horse", 10, "gelding", "chill", ["trail", "barrel"],
          "Retired rodeo star. Just here for the good hay and better company.", 15.1,
          coat="#9a6a3a", mane="#5a3a1a", marking="star", stable="Open Range", distance_km=45),
        H(16, "Thor", "Norwegian Fjord", 5, "stallion", "playful", ["driving", "trail"],
          "Viking hair, big smile. My mane stands up on its own, no gel.", 14.1,
          coat="#c2a878", mane="#4a4038", marking="none", stable="Seaside Paddock", distance_km=31, verified=True),
        H(17, "Blaze", "Tennessee Walker", 7, "gelding", "chill", ["trail", "shows"],
          "Smoothest gait in the county. I'll sweep you off all four feet.", 15.3,
          coat="#7a3020", mane="#e8d8b0", marking="blaze", stable="Meadowbrook", distance_km=6),
        H(18, "Zephyr", "Lipizzaner", 6, "stallion", "stoic", ["dressage", "jumping"],
          "Born dark, turned brilliant white. Airs above the ground, feelings below.", 15.2,
          coat="#f0f0f4", mane="#d0d0d8", marking="none", stable="Highland Stables", distance_km=20, verified=True),
        H(19, "Bandit", "Paint Horse", 5, "stallion", "spirited", ["barrel", "racing"],
          "Two-toned troublemaker with a heart of gold.", 15.0,
          coat="#6a4a30", mane="#e8e0d0", marking="spots", stable="Open Range", distance_km=40),
        H(20, "Shadow", "Friesian", 8, "gelding", "stoic", ["dressage", "driving"],
          "Tall, dark, and dramatic. My mane has its own fan club.", 16.2,
          coat="#26262b", mane="#111114", marking="none", stable="Churchill Barn", distance_km=9, verified=True),
    ]


if __name__ == "__main__":
    engine = StallionSwipe(demo_herd())

    print("=== StallionSwipe deck for Bella (#2) ===")
    for horse, score in engine.deck_for(2):
        flag = " \u2713" if horse.verified else ""
        print(f"  {horse.photo} {horse.name:12}{flag:2} {horse.breed:14} "
              f"{horse.distance_km:>3}km  compatibility {score}")

    print("\n=== Simulating swipes ===")
    engine.swipe(2, 1, True)                 # Bella likes Seabiscuit
    m = engine.swipe(1, 2, True)             # Seabiscuit likes Bella back
    print(f"  Seabiscuit <-> Bella match? {m}")

    engine.swipe(2, 8, True)
    m = engine.swipe(8, 2, True)             # Bella <-> Luna
    print(f"  Bella <-> Luna match? {m}")

    m = engine.swipe(4, 3, True)             # Willow likes Duke (one-sided)
    print(f"  Willow -> Duke match? {m}")

    print("\n=== Bella chats up her matches ===")
    engine.send_message(2, 1, "Neigh there! Trail ride this weekend?")
    engine.send_message(1, 2, "Foal sure, sounds hay-mazing.")
    for msg in engine.thread(1, 2):
        who = engine.herd[msg.from_id].name
        print(f"  {who}: {msg.text}")

    print("\n=== Bella's matches (best first) ===")
    for horse in engine.matches_for(2):
        print(f"  {horse.photo} It's a match with {horse.name}!")
