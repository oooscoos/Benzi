# Bug-fix benchmark

The harness and the complete run log behind
[benzi.fly.dev/benchmark](https://benzi.fly.dev/benchmark) — and its companion
[full record](https://benzi.fly.dev/benchmark_full), which lists every task's
verbatim prompt and all 423 runs.

**This is a vendor-run benchmark.** We built it, we chose the bugs, and Benzi is
ours. That is a reason to be suspicious, so everything needed to check the claims
is here: the harness, the task definitions, and every run ever recorded — the
failures, the superseded runs and the bugs we lose included.

## What it measures

Twenty-four real, already-fixed bugs from real open-source repositories across
eleven languages. Each arm gets the same checkout at the buggy commit, the same
issue text, and the same model. The only variable is the harness driving it.

| arm | what it is |
|---|---|
| `control` | Claude Code CLI |
| `benzi_product` | Benzi |
| `opencode` | OpenCode |
| `aider` | Aider (two exploratory runs only; not on the published page) |

## How a task is built

1. **Pick a real fix** — a merged commit repairing a genuine bug and shipping a
   test that proves it. Its **parent** is the buggy state, and that parent is what
   every arm is handed.
2. **Write the prompt from the symptom** — what a user would observe, and what
   must change. It never names the function to edit. Every prompt is reproduced
   verbatim on the full-record page so this can be checked rather than trusted.
3. **Hide the answer** — the fix is in the repository's future, but history up to
   the parent is still a searchable index, so for the duration of a run `.git` is
   renamed and hidden in **both the worktree and the base clone**. This was added
   after an agent was caught reading a fix out of the base clone.
4. **Grade with the repository's own tests** — the target test that failed on the
   parent must pass, and nothing previously passing may break. Fixing the target
   while breaking a neighbour is recorded as a regression, not a solve.
5. **Run arms back to back** on one machine, so provider and machine drift hit
   everything equally.

## Running it

```bash
export ANTHROPIC_API_KEY=...          # control + benzi on sonnet
export DEEPSEEK_API_KEY=...           # only for --benzi-model deepseek
export BENZI_HOME=/path/to/benzi      # defaults to this repo's root
python harness.py --task fmt_4839 --arms control benzi_product --benzi-model sonnet
```

Repositories are cloned into `repos/` and each run gets a fresh worktree under
`wt/`. Results append to `results/runs.jsonl`.

Analysis scripts read that log directly: `board.py` (which run counts per task),
`progress.py` (the three-arm table), `tokens.py` (token and lines-read
breakdown), `make_benchmark.py` (regenerates the published page's numbers).

## Read this before quoting a number

**Expect different numbers than ours.** Per-task variance is roughly 14–16%, and
we have watched the control arm drift 26% between two sessions on the same
machine. A single run of a single task is close to meaningless; the published
figures are totals across 22 timed bugs for exactly that reason. If you get 30%
where we report 41%, that is within the range this benchmark can resolve — not
evidence that either of us cooked it.

**OpenCode runs were capped.** Once a run passed twice the slower of the other
two arms on the same bug, it was stopped — 13 of them were. Those are reported as
*unfinished*, never as failures, and are excluded from every average. It is a
real limitation: we cannot say what OpenCode would have done given unlimited
time, only that it had not finished in twice the time both other harnesses
needed. Cut runs are logged in `results/oc_killed.jsonl`.

**A failed run is never used as a timing baseline** and never averaged into a
speed comparison, because its wall-clock measures how long that arm took to give
up rather than how long the work takes. Such bugs are reported as solve rates
instead. Applied consistently, this cuts both ways: it removes nats-server and
money from the averages, where it helps Benzi, and it is why http-parser counts
as a loss for Benzi (0 of 4 on Sonnet, against Claude Code's 1 of 4).

**Benzi's wall-clock is reported warm on the summary page** — the one-time,
per-repository index build is subtracted, because it is cached after the first
run and a developer fixing their third bug in a repo never pays it. Cold is 38%
faster and warm is 41%; both are stated. Claude Code has no cacheable
equivalent, so nothing comparable is removed from its side. The run log stores
the raw figure plus `index_build_ms`, so either can be recomputed.

**Runs before 2026-08-11 were made on earlier engine versions** and are kept for
completeness, not comparison.

## What is not here

Agent transcripts. A Benzi transcript records every tool call together with its
result, and those results are the index's output verbatim — the card format, the
identifier scheme, the field set. That is the design of the product rather than
evidence about the benchmark, so it stays private. The run log carries the
measurements and none of the shapes.
