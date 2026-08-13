"""DeepSeek progress, in the same shape as progress.py's sonnet table.

    task | OpenCode | Benzi old | old vs OC | Benzi now | now vs OC

The comparison arm here is OPENCODE, not claude code -- that is the only claim
the DeepSeek section of the page makes. OpenCode's runs are fixed history and
are never re-run: re-measuring both sides at once would make any delta
unattributable.

FAILED OPENCODE RUNS ARE MARKED AND EXCLUDED FROM THE TOTALS. money is the live
case: OpenCode "finished" it in 93s without fixing the bug, and averaging that
into a speed comparison understates Benzi (2.5x with it, 2.8x without). This is
the same rule applied to nats-server on the sonnet board, where it cost us a
win -- a rule that only gets applied when it flatters us is not a rule.
"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NOW_FROM = "2026-08-12T21:45"          # the fresh benzi/deepseek batch
OLD_LO, OLD_HI = "2026-08-11T17:22", "2026-08-11T19:00"
SHORT = {"mux_hostport_vars": "mux", "addressable_template_nonstring": "addressable",
         "commonscli_npe": "commons-cli", "csvhelper_nullable": "CsvHelper",
         "yamlcpp_base64": "yaml-cpp", "cjson_null_deref": "cJSON",
         "jsoup_negative_nth_child": "jsoup", "gson_duplicate_key_null": "gson",
         "money_divide_by_zero": "money", "dayjs_duration_round": "dayjs"}
ORDER = list(SHORT)

rows = [json.loads(l) for l in open("results/runs.jsonl", encoding="utf-8") if l.strip()]


def pick(task, arm, lo, hi=None, model=None):
    c = [r for r in rows if r["task"] == task and r["arm"] == arm
         and r.get("num_turns") is not None and (model is None or r.get("model") == model)
         and (r.get("ts") or "") >= lo and (hi is None or (r.get("ts") or "") < hi)]
    return sorted(c, key=lambda r: r["ts"])[-1] if c else None


cell = lambda r: ("%.0fs / %dt%s" % (r["wall_s"], r["num_turns"], "" if r.get("solved") else "*")
                  if r else "—")
pct = lambda a, b: "%+.0f%%" % ((a / b - 1) * 100) if (a and b) else "—"

print(f'{"task":<14}{"OpenCode":>13}{"Benzi old":>13}{"old/OC":>9}{"Benzi now":>13}{"now/OC":>9}')
print("-" * 71)
ow = ot = 0.0
w_w = w_t = n_w = n_t = 0.0
n_done = 0
pending = []
oc_failed = []
for t in ORDER:
    o = pick(t, "opencode", OLD_LO, OLD_HI)
    w = pick(t, "benzi_product", OLD_LO, OLD_HI, model="deepseek")
    b = pick(t, "benzi_product", NOW_FROM, model="deepseek")
    if not b:
        pending.append(SHORT[t])
    if o and not o.get("solved"):
        oc_failed.append(SHORT[t])
    line = [SHORT[t], cell(o), cell(w),
            pct(w["wall_s"], o["wall_s"]) if (o and w) else "—",
            cell(b),
            pct(b["wall_s"], o["wall_s"]) if (o and b) else "—"]
    print(f'{line[0]:<14}{line[1]:>13}{line[2]:>13}{line[3]:>9}{line[4]:>13}{line[5]:>9}')
    # totals: OpenCode failures excluded from every arm, so the sets match
    if b and o and o.get("solved"):
        n_done += 1
        ow += o["wall_s"]; ot += o["num_turns"]
        n_w += b["wall_s"]; n_t += b["num_turns"]
        if w:
            w_w += w["wall_s"]; w_t += w["num_turns"]

print("-" * 71)
if n_done:
    print(f'{f"TOTAL ({n_done})":<14}{"%.0fs / %dt" % (ow, ot):>13}'
          f'{"%.0fs / %dt" % (w_w, w_t):>13}{pct(w_w, ow):>9}'
          f'{"%.0fs / %dt" % (n_w, n_t):>13}{pct(n_w, ow):>9}')
    print()
    print(f'  WALL    OpenCode {ow:.0f}s   Benzi old {w_w:.0f}s ({pct(w_w, ow)})   '
          f'now {n_w:.0f}s ({pct(n_w, ow)})')
    print(f'  MULTIPLE  Benzi old {ow/max(w_w,1):.1f}x faster than OpenCode   '
          f'now {ow/max(n_w,1):.1f}x faster')
    print(f'  TURNS   OpenCode {ot:.0f}   old {w_t:.0f}   now {n_t:.0f}   '
          f'({ot/max(n_t,1):.1f}x fewer calls than OpenCode)')
    print(f'  old -> now: wall {pct(n_w, w_w)}, turns {pct(n_t, w_t)}')
else:
    print("  (no completed runs yet)")
if oc_failed:
    print(f'\n  * OpenCode FAILED (bug not fixed) on: {", ".join(oc_failed)} -- shown as a row, '
          f'excluded from every total, since timing a fix against a give-up is not a comparison')
if pending:
    print(f'\n  remaining ({len(pending)}): {", ".join(pending)}')
