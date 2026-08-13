"""Progress table for the running full-24 rerun, in the standing format:

    task | control | website | web vs ctrl | Benzi now | now vs ctrl

plus aggregates over the tasks completed so far.

WHICH ROW IS WHICH
  control  -- the 3-arm sweep of 2026-08-11 19:20+, except mux, whose control
              was rerun 2026-08-12 08:15 (the 184s row it replaced was the
              slowest of 5 that day). NOT rerun today: control's code did not
              change, so re-measuring it spends money on the same number.
  website  -- the benzi run currently published on benzi.fly.dev/benchmark.
  now      -- the fresh 2026-08-12 17:03+ run.

The vs-control columns carry a caveat that belongs with them: control drifted
26% between two sessions on 08-11, and today's benzi runs are NOT interleaved
with it. The clean comparison here is website -> now (same arm, same tasks).
"""
import collections
import io
import json
import statistics as st
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
MD = "--md" in sys.argv

ORDER = ["addressable_template_nonstring", "mux_hostport_vars", "commonscli_npe",
         "cjson_null_deref", "jsoup_negative_nth_child", "yamlcpp_base64",
         "csvhelper_nullable", "gson_duplicate_key_null", "money_divide_by_zero",
         "dayjs_duration_round", "fmt_4839", "hashie_deep_merge_dup",
         "rich_softwrap_style_newline", "sqlglot_7920", "scrapy_proxy_auth_leak",
         "zod_pipe_payload_flag", "semver_prerelease", "nlohmannjson_diagnostic_offsets",
         "quartznet_misfire_reschedule", "marked_lexer_linebreaks",
         "httpparser_line_folding", "natsserver_oversized_publish_raft",
         "tspattern_ismatching", "sqlparser_exponential_backtrack"]
SHORT = {"addressable_template_nonstring": "addressable", "mux_hostport_vars": "mux",
         "commonscli_npe": "commons-cli", "cjson_null_deref": "cJSON",
         "jsoup_negative_nth_child": "jsoup", "yamlcpp_base64": "yaml-cpp",
         "csvhelper_nullable": "CsvHelper", "gson_duplicate_key_null": "gson",
         "money_divide_by_zero": "money", "dayjs_duration_round": "dayjs",
         "fmt_4839": "fmt", "hashie_deep_merge_dup": "hashie",
         "rich_softwrap_style_newline": "rich", "sqlglot_7920": "sqlglot",
         "scrapy_proxy_auth_leak": "scrapy", "zod_pipe_payload_flag": "zod",
         "semver_prerelease": "semver", "nlohmannjson_diagnostic_offsets": "nlohmann/json",
         "quartznet_misfire_reschedule": "quartznet", "marked_lexer_linebreaks": "marked",
         "httpparser_line_folding": "http-parser",
         "natsserver_oversized_publish_raft": "nats-server",
         "tspattern_ismatching": "ts-pattern",
         "sqlparser_exponential_backtrack": "sqlparser"}

# The FRESH full-24, started 18:04:54. Must NOT be 17:03: that was the earlier
# run paused at 11/24, and a cutoff that early silently mixes its stale rows
# into "Benzi now" -- the 11 completed tasks would read as current when they
# predate this engine's index changes entirely.
NOW_FROM = "2026-08-12T18:04"
rows = [json.loads(l) for l in open("results/runs.jsonl", encoding="utf-8") if l.strip()]


def pick(task, arm, lo, hi=None):
    c = [r for r in rows if r["task"] == task and r["arm"] == arm
         and r.get("model") == "sonnet" and r.get("num_turns") is not None
         and (r.get("ts") or "") >= lo and (hi is None or (r.get("ts") or "") < hi)]
    return sorted(c, key=lambda r: r["ts"])[-1] if c else None


def control_of(t):
    if t == "natsserver_oversized_publish_raft":
        # nats-server is the one task where control is unreliable: 2 solves in
        # 4 attempts, and the run the normal window would pick (902s, 08-12
        # 07:27) is one of the FAILURES -- a time that measures how long it
        # took to give up, not how long it took to fix. So the baseline is the
        # mean of control's two SOLVED runs, which is the only pair that
        # measures the same outcome our run is being scored on.
        #
        # State the spread whenever this number is quoted: 388.0s/41t and
        # 1346.7s/71t, from DIFFERENT sessions (08-07 and 08-11), and control
        # drifted 26% between sessions. A 3.5x spread means the mean (867s)
        # describes neither run well -- it is the least-bad baseline available,
        # not a precise one.
        won = [r for r in rows if r["task"] == t and r["arm"] == "control"
               and r.get("model") == "sonnet" and r.get("solved")
               and r.get("num_turns") is not None]
        if won:
            n = len(won)
            return {"task": t, "arm": "control", "solved": True,
                    "ts": "mean of %d solved runs" % n,
                    "wall_s": sum(r["wall_s"] for r in won) / n,
                    "num_turns": round(sum(r["num_turns"] for r in won) / n),
                    "cost_usd": sum((r.get("cost_usd") or 0) for r in won) / n}
    if t == "mux_hostport_vars":
        return pick(t, "control", "2026-08-12T08:00", "2026-08-12T12:00")
    # Upper bound is 08:00, NOT midnight. The 08-11 sweep did not finish on
    # 08-11: it ran straight through to 07:27 the next morning, so a "< 00:00"
    # cutoff silently cut it in half and orphaned TEN control runs (hashie,
    # semver, quartznet, nlohmann/json, zod, marked, ts-pattern, sqlparser,
    # nats-server, chrono) -- nearly every task in the back half of the board,
    # each of which then rendered as a blank control cell rather than an error.
    # Verified before widening: the two ranges share ZERO tasks (14 + 10 = 24
    # distinct), so this only fills blanks and cannot change which run any
    # already-populated row was compared against. 08:00 also stays clear of
    # mux's rerun window above.
    return pick(t, "control", "2026-08-11T19:20", "2026-08-12T08:00")


def website_of(t):
    if t == "fmt_4839":                       # the board uses the 596s run
        return pick(t, "benzi_product", "2026-08-11T21:00", "2026-08-11T22:00")
    return pick(t, "benzi_product", "2026-08-11T18:54", "2026-08-12T09:00")


def cell(r):
    """A run's wall/turns, with UNSOLVED runs marked.

    Without this, a failed run renders identically to a successful one and its
    time silently becomes a baseline. nats-server is the live example: control
    is 2-for-4 there, and the run control_of() picks (902s, 08-12 07:27) is one
    of the FAILURES -- so "% vs control" on that row would compare our fix
    against an arm that spent 902s and did not fix it. A time is only a
    baseline if the bug actually got fixed; otherwise it measures how long
    something gave up.
    """
    if not r:
        return "—"
    return "%.0fs / %dt%s" % (r["wall_s"], r["num_turns"],
                              "" if r.get("solved") else "*")
pct = lambda a, b: "%+.0f%%" % ((a / b - 1) * 100)

if MD:
    print("| task | control | website | web vs ctrl | Benzi now | now vs ctrl |")
    print("|---|---|---|---|---|---|")
else:
    print(f'{"task":<14}{"control":>13}{"website":>13}{"web/ctrl":>10}{"Benzi now":>13}{"now/ctrl":>10}')
    print("-" * 74)

cw = ww = nw = 0.0
ct = wt = nt = 0
cc = wc = nc = 0.0
n_done = 0
now_ratios, web_ratios = [], []
solved_now = solved_web = solved_ctl = 0
pending = []

# Deliberately NOT run this session, by request -- cancelled 18:29 at 414s
# (2.08x control). Not a censored measurement: fmt is slow because of a known
# index gap (include/fmt/format.h, 4415 lines -> 25 nodes, zero Class/Struct)
# that this engine change does not touch, so the run could only re-confirm a
# number we already have eight of. It gets a ROW, not a slot in "remaining":
# a skipped task hidden among pending ones reads as still-coming, and the
# aggregates below must not quietly count 23 tasks while looking like 24.
# Shown as a row, EXCLUDED from every aggregate. nats-server is the one task
# where neither arm is dependable -- control solved 2 of 4, benzi 1 of 2 -- so
# its baseline has to be the mean of control's two solved runs (388s and
# 1347s, 3.5x apart, different sessions). A row built on that is worth looking
# at; a TOTAL built on it would launder a guess into a headline number.
NO_AGG = {"natsserver_oversized_publish_raft"}

SKIPPED = {"httpparser_line_folding"}
# fmt UN-SKIPPED: the traced rerun on the fixed engine landed 223.4s / 30t,
# solved -- its best run ever (previous best 258s, median 476s, and 985s
# earlier the same evening). The trace shows why, and it is the cleanest
# before/after the index has produced: get_callers("format.h::write_int")
# answered instead of erroring, and the agent went from 166 tool calls
# (read_source 65, edit_lines 58, rollback 13) to 34 (11 / 2 / 0).
# http-parser stays out: a sonnet failure, 0/4, its only benzi solves deepseek.
# sqlparser and ts-pattern were UN-skipped: both were cancelled during the
# 24-run, but the post-fix recheck gave each a real current-engine row, so they
# are measurements again rather than gaps. fmt stays skipped -- its recheck hit
# the 2x-control gate (398s) and a timeout records no row at all; the traced
# rerun at a 950s gate is what will fill it. http-parser stays skipped as a
# sonnet failure (0/4 on sonnet; its only benzi solves were deepseek).
# sqlparser cancelled 20:35 at ~11 min against its own history of two SOLVES at
# 199s and 315s. Distinct failure mode from ts-pattern: ZERO edits and ZERO
# builds in eleven minutes -- no rollback ledger was ever created and no
# target/ dir existed, so it never compiled anything. The process was ~97%
# idle (29.8s CPU, most of it the index build), i.e. reading and searching
# without converging. NOTE: cancelled runs leave NO trace file -- the harness
# only writes _benzi.jsonl after benzi_headless returns -- so unlike ts-pattern
# (whose live edit ledger explained everything) this one is unexplained, and
# there is nothing on disk to go back to.
# ts-pattern cancelled 20:24 at ~21 min, against its own history of four
# SOLVES at 183s/220s/469s/595s. Its live edit ledger showed no stall at all --
# 62 edits, median 15s apart, largest gap 72s -- just an expensive method: 43
# of those edits were probes into scratch files it created (scratch-debug,
# scratch2/3/4.ts), each needing a tsc compile of a heavy type-level library
# to read the resulting type error. Legitimate for a type-inference bug,
# but a 21-minute outlier against four fast solves is not a number worth
# spending another 10 minutes to finish.
# http-parser cancelled 19:33 at 1184s -- 3x its own worst previous run (395s)
# and longer than control's only successful solve. Benzi has never solved it:
# 0 for 4 (186s, 185s, 219s, 395s, all failed), and control solved it once in
# four tries (856s). board.py treats it as SOLVED_ONLY, so a fifth failure
# would not have counted toward the published board at all.

for t in ORDER:
    c, w, b = control_of(t), website_of(t), pick(t, "benzi_product", NOW_FROM)
    if not b:
        if t in SKIPPED:
            row = [SHORT[t], cell(c), cell(w),
                   pct(w["wall_s"], c["wall_s"]) if (c and w) else "—",
                   "SKIPPED", "—"]
            if MD:
                print("| " + " | ".join(row) + " |")
            else:
                print(f'{row[0]:<14}{row[1]:>13}{row[2]:>13}{row[3]:>10}'
                      f'{row[4]:>13}{row[5]:>10}')
            continue
        pending.append(SHORT[t])
        continue
    line = [SHORT[t], cell(c), cell(w),
            pct(w["wall_s"], c["wall_s"]) if (c and w) else "—",
            cell(b),
            pct(b["wall_s"], c["wall_s"]) if c else "—"]
    if t in NO_AGG:
        line[0] += "~"
    if MD:
        print("| " + " | ".join(line) + " |")
    else:
        print(f'{line[0]:<14}{line[1]:>13}{line[2]:>13}{line[3]:>10}{line[4]:>13}{line[5]:>10}')
    # SHOWN but NOT AGGREGATED. The row is real and worth seeing; the totals
    # are a claim, and a task whose baseline is the mean of two runs 3.5x apart
    # cannot support one. Excluding it from the aggregate is not hiding it --
    # it stays visible with a ~ and its own footnote.
    if t in NO_AGG:
        continue
    n_done += 1
    if c:
        cw += c["wall_s"]; ct += c["num_turns"]; cc += c.get("cost_usd") or 0
        solved_ctl += bool(c["solved"])
        now_ratios.append(b["wall_s"] / c["wall_s"])
    if w:
        ww += w["wall_s"]; wt += w["num_turns"]; wc += w.get("cost_usd") or 0
        solved_web += bool(w["solved"])
        if c:
            web_ratios.append(w["wall_s"] / c["wall_s"])
    nw += b["wall_s"]; nt += b["num_turns"]; nc += b.get("cost_usd") or 0
    solved_now += bool(b["solved"])

if not n_done:
    print("  (no rows yet)")
    raise SystemExit

tot = [f"TOTAL ({n_done})", "%.0fs / %dt" % (cw, ct), "%.0fs / %dt" % (ww, wt),
       pct(ww, cw), "%.0fs / %dt" % (nw, nt), pct(nw, cw)]
if MD:
    print("| " + " | ".join("**" + x + "**" for x in tot) + " |")
else:
    print("-" * 74)
    print(f'{tot[0]:<14}{tot[1]:>13}{tot[2]:>13}{tot[3]:>10}{tot[4]:>13}{tot[5]:>10}')

print()
# COLD vs WARM. Every benchmark run gets a fresh worktree, so benzi rebuilds
# the index from scratch 24 times; a real user pays that once per repo and it
# is cached in .benzi afterwards. The published page reports BOTH for exactly
# this reason ("21% faster rather than 25%" -- benchmark.html), so a progress
# report that only shows cold is not comparable to the board.
# NB: the website column CANNOT be warm-adjusted -- index_build_ms did not
# exist when it ran, so its index time is inside its wall and unrecoverable.
# It is therefore a COLD number, and comparing it to a warm "now" would flatter
# us. Cold-vs-cold is the honest like-for-like line.
idx_now = sum((pick(t, "benzi_product", NOW_FROM) or {}).get("index_build_ms") or 0
              for t in ORDER) / 1000.0
warm = nw - idx_now
print(f'  WALL    control {cw:.0f}s   website {ww:.0f}s ({pct(ww, cw)})   now {nw:.0f}s ({pct(nw, cw)})')
print(f'  COLD/WARM   now cold {nw:.0f}s ({pct(nw, cw)} vs ctrl)   '
      f'now WARM {warm:.0f}s ({pct(warm, cw)} vs ctrl)   '
      f'[index {idx_now:.0f}s, avg {idx_now/max(n_done,1):.1f}s/task]')
print(f'              website {ww:.0f}s is COLD too ({pct(ww, cw)}) -- like-for-like is '
      f'cold vs cold: {pct(nw, cw)} vs {pct(ww, cw)}')
print(f'  TURNS   control {ct}      website {wt} ({pct(wt, ct)})      now {nt} ({pct(nt, ct)})')
print(f'  COST    control ${cc:.2f}  website ${wc:.2f} ({pct(wc, cc)})  now ${nc:.2f} ({pct(nc, cc)})')
print(f'  SOLVED  control {solved_ctl}/{n_done}   website {solved_web}/{n_done}   now {solved_now}/{n_done}')
if now_ratios:
    print(f'  PER-TASK vs control   website mean {st.mean(web_ratios):.2f}x'
          f'   now mean {st.mean(now_ratios):.2f}x  median {st.median(now_ratios):.2f}x'
          f'   wins {sum(1 for r in now_ratios if r < 1)}/{len(now_ratios)}')
print(f'  website -> now: wall {pct(nw, ww)}, turns {pct(nt, wt)}')
unsolved = [(SHORT[t], arm) for t in ORDER if t not in SKIPPED
            for arm, r in (("control", control_of(t)), ("website", website_of(t)),
                           ("now", pick(t, "benzi_product", NOW_FROM)))
            if r and not r.get("solved")]
if unsolved:
    print(f'\n  * UNSOLVED -- the bug was NOT fixed, so this time is not a '
          f'like-for-like baseline: {", ".join(f"{t} ({a})" for t, a in unsolved)}')
shown_no_agg = [SHORT[t] for t in NO_AGG
                if pick(t, "benzi_product", NOW_FROM) and t in ORDER]
if shown_no_agg:
    print(f'\n  ~ shown but EXCLUDED from all aggregates: {", ".join(shown_no_agg)} '
          f'-- control solved 2/4 there and benzi 2/3; the baseline is the mean '
          f'of control\'s two solves (388s, 1347s), too wide to total against')
if pending:
    print(f'\n  remaining ({len(pending)}): {", ".join(pending)}')
