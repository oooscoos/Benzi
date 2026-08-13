"""Token + lines-read aggregate: control vs website vs now.

WHY THIS TABLE EXISTS: "cheaper" on the board is a single cost_usd number, and
that number hides which lever moved. Cost here is dominated by CACHE_READ --
the whole conversation prefix, re-billed every turn -- not by what the model
generates. So an arm can be cheaper for two very different reasons: it took
fewer turns (fewer prefix re-reads), or it carried a smaller prefix per turn
(less source pasted into the transcript). Those are different claims about the
product, and only this breakdown separates them.

  in_tokens    fresh input, uncached (tiny -- effectively noise here)
  cache_write  prefix written to cache the first time it appears
  cache_read   prefix re-read on every subsequent turn  <- the mass
  out_tokens   what the model GENERATES: reasoning + tool-call args + prose

LINES READ: benzi records source_lines_read on its own row, so website and now
both come straight from runs.jsonl. Control does not record it -- it has to be
reconstructed from saved stream-json transcripts, which are overwritten per
task+arm on rerun. Where that reconstruction is unavailable the cell says so
rather than showing a zero, because a zero would read as "control read nothing".
"""
import io
import json
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ORDER = ["addressable_template_nonstring", "mux_hostport_vars", "commonscli_npe",
         "cjson_null_deref", "jsoup_negative_nth_child", "yamlcpp_base64",
         "csvhelper_nullable", "gson_duplicate_key_null", "money_divide_by_zero",
         "dayjs_duration_round", "fmt_4839", "hashie_deep_merge_dup",
         "rich_softwrap_style_newline", "sqlglot_7920", "scrapy_proxy_auth_leak",
         "zod_pipe_payload_flag", "semver_prerelease", "nlohmannjson_diagnostic_offsets",
         "quartznet_misfire_reschedule", "marked_lexer_linebreaks",
         "httpparser_line_folding", "natsserver_oversized_publish_raft",
         "tspattern_ismatching", "sqlparser_exponential_backtrack"]
# fmt is back IN: its traced rerun on the fixed engine landed 223.4s/30t. Only
# the two untimed bugs stay out -- http-parser (neither arm solves it reliably)
# and nats-server (handled as a solve-rate row, not a stopwatch row).
SKIPPED = {"httpparser_line_folding", "natsserver_oversized_publish_raft"}
NOW_FROM = "2026-08-12T18:04"

rows = [json.loads(l) for l in open("results/runs.jsonl", encoding="utf-8") if l.strip()]


def pick(task, arm, lo, hi=None):
    c = [r for r in rows if r["task"] == task and r["arm"] == arm
         and r.get("model") == "sonnet" and r.get("num_turns") is not None
         and (r.get("ts") or "") >= lo and (hi is None or (r.get("ts") or "") < hi)]
    return sorted(c, key=lambda r: r["ts"])[-1] if c else None


def control_of(t):
    if t == "mux_hostport_vars":
        return pick(t, "control", "2026-08-12T08:00", "2026-08-12T12:00")
    return pick(t, "control", "2026-08-11T19:20", "2026-08-12T08:00")


def website_of(t):
    if t == "fmt_4839":
        return pick(t, "benzi_product", "2026-08-11T21:00", "2026-08-11T22:00")
    return pick(t, "benzi_product", "2026-08-11T18:54", "2026-08-12T09:00")


# Only tasks where ALL THREE arms have a row -- an aggregate built from
# different task sets per column would compare different work.
FIELDS = ("in_tokens", "cache_write", "cache_read", "out_tokens", "cost_usd",
          "num_turns", "wall_s", "source_lines_read")
agg = {a: dict.fromkeys(FIELDS, 0.0) for a in ("control", "website", "now")}
n = 0
paired = []
for t in ORDER:
    if t in SKIPPED:
        continue
    c, w, b = control_of(t), website_of(t), pick(t, "benzi_product", NOW_FROM)
    if not (c and w and b):
        continue
    n += 1
    paired.append(t)
    for arm, r in (("control", c), ("website", w), ("now", b)):
        for f in FIELDS:
            agg[arm][f] += (r.get(f) or 0)

if not n:
    print("no fully-paired tasks yet")
    raise SystemExit

pct = lambda v, base: ("  —  " if not base else "%+.0f%%" % ((v / base - 1) * 100))
k = lambda v: f"{v/1000:,.0f}K" if v >= 1000 else f"{v:,.0f}"

print(f"TOKENS + LINES READ -- {n} tasks with all three arms present")
print(f"(fmt excluded: skipped this session)\n")
print(f'{"":<16}{"control":>12}{"website":>12}{"vs ctrl":>9}{"now":>12}{"vs ctrl":>9}{"web->now":>10}')
print("-" * 80)
LABELS = [("in_tokens", "in (uncached)"), ("cache_write", "cache write"),
          ("cache_read", "cache read"), ("out_tokens", "out (generated)")]
for f, label in LABELS:
    c, w, b = agg["control"][f], agg["website"][f], agg["now"][f]
    print(f'{label:<16}{k(c):>12}{k(w):>12}{pct(w,c):>9}{k(b):>12}{pct(b,c):>9}{pct(b,w):>10}')

tot = lambda a: sum(agg[a][f] for f in ("in_tokens", "cache_write", "cache_read", "out_tokens"))
c, w, b = tot("control"), tot("website"), tot("now")
print("-" * 80)
print(f'{"TOTAL tokens":<16}{k(c):>12}{k(w):>12}{pct(w,c):>9}{k(b):>12}{pct(b,c):>9}{pct(b,w):>10}')

for f, label, fmt in (("cost_usd", "cost", "$%.2f"), ("num_turns", "turns", "%.0f"),
                      ("wall_s", "wall", "%.0fs")):
    c, w, b = agg["control"][f], agg["website"][f], agg["now"][f]
    print(f'{label:<16}{fmt%c:>12}{fmt%w:>12}{pct(w,c):>9}{fmt%b:>12}{pct(b,c):>9}{pct(b,w):>10}')

# per-turn prefix: the "how heavy is each turn" number, which total tokens alone
# cannot show -- fewer turns shrinks the total even if each turn got fatter.
print()
for a in ("control", "website", "now"):
    t_, r_ = agg[a]["num_turns"], agg[a]["cache_read"]
    print(f'  {a:<9} cache_read/turn {r_/max(t_,1):>10,.0f}   out/turn {agg[a]["out_tokens"]/max(t_,1):>7,.0f}')

# LINES OF SOURCE READ, same 3 arms, same paired task set.
# Control does not record it, so its number is reconstructed from the saved
# stream-json: every Read tool_use matched to its tool_result, counting the
# numbered lines that came BACK. That is what the model was actually shown --
# a Read with no offset returns up to 2000 lines whether it wanted them or not,
# which is precisely the difference being measured.
import glob
import os
import re


def control_lines(path):
    read_ids, lines, calls = set(), 0, 0
    for raw in open(path, encoding="utf-8", errors="replace"):
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for b in ((ev.get("message") or {}).get("content") or []):
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use" and b.get("name") == "Read":
                read_ids.add(b.get("id"))
                calls += 1
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in read_ids:
                c = b.get("content")
                if isinstance(c, list):
                    c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                if isinstance(c, str):
                    lines += len(re.findall(r"^\s*\d+\t", c, re.M)) or c.count("\n")
    return lines, calls


print("\nLINES OF SOURCE READ")
cl_tot = cr_tot = 0
missing = []
for t in paired:
    hits = glob.glob(f"results/transcripts/{t}_control_*_control.jsonl")
    if not hits:
        missing.append(t)
        continue
    l, r = control_lines(sorted(hits, key=os.path.getmtime)[-1])
    cl_tot += l
    cr_tot += r
wl, bl = agg["website"]["source_lines_read"], agg["now"]["source_lines_read"]
wr = sum(((pick(t, "benzi_product", "2026-08-11T18:54", "2026-08-12T09:00") or {})
          .get("tools") or {}).get("read_source", 0) for t in paired)
br = sum(((pick(t, "benzi_product", NOW_FROM) or {}).get("tools") or {})
         .get("read_source", 0) for t in paired)
print(f'{"":<16}{"lines":>10}{"reads":>8}{"lines/read":>12}{"vs ctrl":>9}')
print("-" * 56)
for label, li, rd in (("control", cl_tot, cr_tot), ("website", wl, wr), ("now", bl, br)):
    print(f'{label:<16}{li:>10,.0f}{rd:>8.0f}{li/max(rd,1):>12,.0f}{pct(li, cl_tot):>9}')
if missing:
    print(f'  NOTE: no control transcript for {len(missing)} paired task(s), so the '
          f'control row covers fewer tasks than website/now: {", ".join(missing)}')
