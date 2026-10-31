# Benzi on SWE-bench Verified: second October run

**413 of 500 resolved (82.6%), pass@1, on DeepSeek V4.1-Flash, for $9.26 total: 2.2¢ per resolved instance.**

The second full run of October (October 30–31, 2026), on a later build than the [first October run](../swebench-october/SWE_BENCH_REPORT.md) (412/500, $12.96). One configuration, one attempt per instance, no ensembling, no test-time selection, graded by the official SWE-bench harness. This report describes the system, the setup, the results, and how to reproduce them.

---

## 1. Headline results

| | |
|---|---|
| **Resolved** | **413 / 500 (82.6%)** |
| Attempts per instance | 1 (pass@1) |
| Model | DeepSeek V4.1-Flash, thinking mode at its default effort |
| Total generation cost, all 500 | $9.26 |
| Cost per resolved instance | $0.022 |
| Model turns: total / median per instance | 13,281 / 20.5 |
| Input tokens served from prompt cache | 97.6% |
| Output tokens, total (of which reasoning) | 8.6M (6.3M) |

Costs are DeepSeek list prices at the standard (off-peak) rates, over measured tokens.

Grading: `swebench.harness.run_evaluation` (swebench 5.0.2), official per-instance Docker images, official Hugging Face dataset (`SWE-bench/SWE-bench_Verified`). An empty prediction counts as unresolved.

### By repository

| Repository | Instances | Resolved | Rate |
|---|---:|---:|---:|
| flask | 1 | 1 | 100.0% |
| scikit-learn | 32 | 31 | 96.9% |
| pytest | 19 | 17 | 89.5% |
| django | 231 | 198 | 85.7% |
| matplotlib | 34 | 28 | 82.4% |
| xarray | 22 | 18 | 81.8% |
| sympy | 75 | 59 | 78.7% |
| sphinx | 44 | 34 | 77.3% |
| astropy | 22 | 17 | 77.3% |
| pylint | 10 | 5 | 50.0% |
| requests | 8 | 4 | 50.0% |
| seaborn | 2 | 1 | 50.0% |

## 2. The system

Benzi is a code-index agent. Before the model sees anything, a tree-sitter-based compiler parses the whole repository into a queryable map: symbols, call edges with the evidence that resolved them, references, inheritance, and per-scope data and control flow. Ambiguous calls keep their candidate lists instead of a guess, and calls the compiler cannot classify are tagged as declared unknowns. The agent works through 33 tools: structured queries over that index (`profile`, `get_callers`, `backflow`, `trace_path`, `skim_source`, and others), edit tools, and a shell for running the project's own tests.

Every write is syntax-gated against the real language parser: an edit that breaks the parse reverts itself. Every edit that lands returns a receipt: the changed symbol, its callers, how the call graph changed, and how far the lines below the edit moved.

The benchmark configuration is the shipped product, run headless: one agent, one pass. No verifier, no second model, no precomputed analysis of the issue. The model runs in DeepSeek's thinking mode at its default effort, with its reasoning carried across tool calls.

No FAIL_TO_PASS or PASS_TO_PASS test names, files or contents were shown to the agent at solve time. The agent sees the issue text and the repository, nothing else.

## 3. Setup

- **Containers.** Each instance ran inside its official SWE-bench per-instance Docker image, with the Benzi engine and a prebuilt Python runtime mounted read-only. GitHub and PyPI hosts resolved to loopback inside every container, so nothing could fetch the fixed version of itself.
- **Budgets.** No wall-clock timeout was imposed on the agent. Shell commands carry a 10-minute default limit, which the agent can raise.
- **Retries.** No attempt died to infrastructure in this run: no image-pull failures, no API disconnects. Three grading runs hit a harness infrastructure error and were re-graded from scratch. No instance was retried for being wrong; every instance is reported from its one attempt.

## 4. Limitations

- Single configuration, single run, pass@1: no ensembling, no multiple samples, no test-time selection, no cherry-picking.
- All numbers are on DeepSeek V4.1-Flash. The architecture is model-agnostic, but this result is not a claim about other models.

## 5. Reproducibility

The harness entry points are `benzi_headless.py` (the agent, one process per instance) and `benchmark/swebench_docker.py` (container orchestration, mounts, environment). The benchmark configuration is the default one; no environment flags are set. Generation ran on a single EC2 host (Python 3.11); grading used the official harness against the official dataset.

---

*Benzi: an AI coding agent that doesn't read, it queries. [benzi.fly.dev](https://benzi.fly.dev/about) · [github.com/oooscoos/Benzi](https://github.com/oooscoos/Benzi)*
