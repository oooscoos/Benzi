"""How many lines of source did each arm actually read?

Benzi records source_lines_read on its row. Claude Code does not, so its number
is reconstructed from its saved stream-json: match every Read tool_use to its
tool_result and count the lines that came back. That measures what the model was
actually shown, not what it asked for -- a Read with no offset/limit returns up
to 2000 lines whether the model wanted them or not, and that difference is the
whole question here.

Only Read is counted, on both sides. grep/bash output is search, not reading
source, and counting it would compare different things.

CAVEAT: transcripts are overwritten per task+arm on rerun, so this reflects the
most recent run of each task -- which for this sweep is the run in the table.
"""
import collections
import glob
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

MUX = "mux_hostport_vars"


def control_lines(path):
    """(lines_returned, read_calls) from a claude-code stream-json transcript."""
    read_ids, lines, calls = set(), 0, 0
    for raw in open(path, encoding="utf-8", errors="replace"):
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        msg = ev.get("message") or {}
        for b in (msg.get("content") or []):
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
                    # Read renders as "   123\tsource" -- count only numbered lines,
                    # so headers and notices don't inflate the total
                    lines += len(re.findall(r"^\s*\d+\t", c, re.M)) or c.count("\n")
    return lines, calls


rows = [json.loads(l) for l in open("results/runs.jsonl", encoding="utf-8") if l.strip()]
by = collections.defaultdict(dict)
for r in sorted(rows, key=lambda r: r.get("ts") or ""):
    ts = r.get("ts") or ""
    if r["arm"] not in ("control", "benzi_product") or r.get("wall_s") is None:
        continue
    if "2026-08-11T19:10" <= ts < "2026-08-11T19:20":
        continue
    keep = ("2026-08-11T18:54" <= ts < "2026-08-11T19:10") if r["task"] == MUX \
        else (ts >= "2026-08-11T19:20")
    if keep:
        by[r["task"]][r["arm"]] = r

print(f'{"task":<26}{"CC lines":>10}{"CC reads":>10}{"Bz lines":>10}{"Bz reads":>10}{"Bz/CC":>8}')
print("-" * 74)
tc = tb = rc = rb = 0
n = 0
for task, d in by.items():
    c, b = d.get("control"), d.get("benzi_product")
    if not (c and b):
        continue
    hits = glob.glob(f"results/transcripts/{task}_control_*_control.jsonl")
    if not hits:
        print(f'{task[:26]:<26}{"no transcript":>40}')
        continue
    cl, cr = control_lines(sorted(hits, key=os.path.getmtime)[-1])
    bl = b.get("source_lines_read") or 0
    br = (b.get("tools") or {}).get("read_source", 0)
    if not cl:
        print(f'{task[:26]:<26}{0:>10}{cr:>10}{bl:>10}{br:>10}{"n/a":>8}')
        continue
    n += 1
    tc += cl; tb += bl; rc += cr; rb += br
    print(f'{task[:26]:<26}{cl:>10}{cr:>10}{bl:>10}{br:>10}{bl / cl:>7.2f}x')

print("-" * 74)
if n:
    print(f'{f"TOTAL ({n})":<26}{tc:>10}{rc:>10}{tb:>10}{rb:>10}{tb / tc:>7.2f}x')
    print(f'\n  benzi read {(tb - tc) / tc * 100:+.0f}% the source lines claude code did')
    if rc:
        print(f'  lines per read call:   claude code {tc / rc:>6.0f}   benzi {tb / max(rb, 1):>6.0f}')
    print(f'  read calls:            claude code {rc:>6}   benzi {rb:>6}')
