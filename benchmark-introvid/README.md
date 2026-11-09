# Intro video: Claude Code vs Benzi, one question

The two runs behind the head-to-head in Benzi's intro video: the same question about
[Excalidraw](https://github.com/excalidraw/excalidraw), asked of plain Claude Code and of Benzi,
both on Claude Sonnet 5.

> **This question is one of many from our replication of CodeGraph's official benchmark.**
> Every question, every arm (bare Claude Code, CodeGraph, Benzi MCP, Benzi) and four AI judges'
> verdicts: **[varianttech.net/benchmark_codegraph](https://varianttech.net/benchmark_codegraph)**

**Question:** *How does Excalidraw render and update canvas elements?*
**Repo:** excalidraw at commit `6574de6`

| | Claude Code | Benzi |
|---|---|---|
| Model | Claude Sonnet 5 | Claude Sonnet 5 |
| Tool calls | 22 | 21 |
| **Source lines read** | **3,102** | **43** |
| Cost | $0.454 | $0.264 (42% less) |

- **Claude Code** ran plain: a fresh config, no MCP servers, no CLAUDE.md.
- **Benzi** is Benzi's own agent (its headless runner), with a fresh home: no memory, no cache.

**Source lines read** counts every line of source the agent was shown, the same rule as our other
benchmarks. Claude Code: `Read` results (3,063) plus shell commands that print files, such as
`cat`, `sed -n`, `head` and `tail` (39). Benzi: `read_source` results (43: `StaticCanvas.tsx`,
lines 33–75). Directory listings and search results aren't counted for either.

**Cost:** Claude Code's figure is the cost it reported itself. Benzi's is computed from its recorded
token usage at the same Sonnet 5 rates Claude Code's figure uses: $2 / $10 per million input / output
tokens, $0.20 per million cache reads, $2.50 per million cache writes.

## Files

- [claude-code/trace.md](claude-code/trace.md): every tool call and its result, then the final answer
- [claude-code/stream.jsonl](claude-code/stream.jsonl): the raw `claude -p --output-format stream-json` output
- [benzi/trace.md](benzi/trace.md): every tool call and its result, then the final answer
- [benzi/run.json](benzi/run.json): the raw run record from Benzi's headless runner (calls, results, token usage, answer)

Local paths in the traces are shortened (`C:\work\excalidraw`). Benzi's runner keeps the first 4,000
characters of each tool result in its log; the model saw every result in full.
