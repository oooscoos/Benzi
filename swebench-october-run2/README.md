# SWE-bench Verified submission kit (October, run 2)

The complete materials behind Benzi's second October SWE-bench Verified run (October 30–31, 2026): 413/500 (82.6%), pass@1, DeepSeek V4.1-Flash. First October run: [swebench-october/](../swebench-october/) (412/500).

- [SWE_BENCH_REPORT.md](SWE_BENCH_REPORT.md): the technical report
- [all_preds.jsonl](all_preds.jsonl): all 500 predictions, one attempt each (pass@1)
- [trajs/](trajs/): per-instance tool-call sequences, recorded during inference
- [metadata.yaml](metadata.yaml): the run's metadata

## Against mini-swe-agent

Same 500 instances, same model (DeepSeek V4.1-Flash), one attempt each, graded by the official harness. The mini-swe-agent run's own kit: [swebench-october-SWEMINIAGENT/](../swebench-october-SWEMINIAGENT/).

| | Benzi, run 2 | Benzi, run 1 | mini-swe-agent |
|---|---|---|---|
| **Resolved** | **413 (82.6%)** | 412 (82.4%) | 410 (82.0%) |
| Cost, all 500 | $9.26 | $12.96 | $6.39 |
| Lines of code viewed | 326,928 | 371,301 | 645,752 |
| Model calls | 13,281 | 14,167 | 12,065 |
| Tool calls | 16,138 | 17,970 | 16,316 |
| Output tokens | 8.65M | 13.46M | 6.29M |
| Input tokens served from cache | 97.6% | 97.6% | 96.8% |

Lines of code viewed counts every line of source the agent was shown: `read_source` results plus the output of shell commands that view files (`cat`, `sed -n`, `head`, `tail`, `nl`, `less`, `more`). For mini-swe-agent, a long output counts as the head and tail it was shown. mini-swe-agent viewed 1.98× as many lines as Benzi's second run. Costs are DeepSeek list prices at the standard (off-peak) rates.
