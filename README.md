<!--
  NOTE: the VS Code Marketplace requires ABSOLUTE image URLs -- relative paths
  render on GitHub but break on the Marketplace page, so the raw GitHub URLs
  below are intentional.
-->
<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/icon.png" width="120" alt="Benzi">
</p>

<h1 align="center">Benzi</h1>

<p align="center"><b>An AI coding agent that doesn't read — it <i>queries</i>.</b></p>

<p align="center">
  <a href="https://benzi.fly.dev/horse_tinder">Horse&nbsp;Tinder&nbsp;Demo</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev/about">Website</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev">Live demo</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev/benchmark">Benchmark</a> &nbsp;·&nbsp;
  <a href="https://marketplace.visualstudio.com/items?itemName=varianttech.benzi">VS&nbsp;Code&nbsp;Marketplace</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/demo.gif" width="700" alt="Benzi demo">
  <br>
  <sub>Select a symbol in the graph → ask about it → Benzi queries the map and answers.</sub>
</p>

---

## What is Benzi

Most AI coding agents dump a repository into a context window and hope the model finds what matters. Benzi works differently: before answering anything, a real compiler — built on tree-sitter — parses every file in the project and resolves it into a precise, queryable map. Every symbol, every call edge, every reference, every class in its inheritance chain. One pass, done.

The agent then navigates that map with structured tools — not grep, not embeddings. Where a function is defined, who calls it, what feeds its parameters, and where its return value ends up are each one O(1) lookup, every time.

## SWE-bench Verified

The full SWE-bench Verified set — 500 real GitHub issues from twelve Python repositories — run end to end on **DeepSeek v4-flash**, one attempt per instance, graded by the official `swebench.harness.run_evaluation` inside its own per-instance Docker images, with network access to GitHub and PyPI blocked inside every container.

| | |
|---|---|
| **Resolved** | **390 / 500 — 78.0%** |
| Total cost, all 500 instances | $37.33 |
| Cost per instance resolved | $0.096 |
| Source lines read (total / median) | 231,574 / 379 |
| Model turns (total / median) | 16,091 / 27 |
| Input tokens served from cache | 97% |
| Output tokens | 22.0M |

Full technical report: [swebench/SWE_BENCH_REPORT.md](swebench/SWE_BENCH_REPORT.md) ([web version](https://benzi.fly.dev/report)). Every instance's cost, tokens, turns, and lines read: [benzi.fly.dev/benchmark_swebench](https://benzi.fly.dev/benchmark_swebench). The cross-harness efficiency comparison (lines read, wall clock, cost vs. Claude Code and a plain DeepSeek harness on 24 bugs): [benzi.fly.dev/benchmark](https://benzi.fly.dev/benchmark).

## How it works

1. **Compile.** Tree-sitter parses every file; imports are resolved, class ancestry built, every identifier traced to its definition. The output is an index, not a blob of text.
2. **Query.** The agent answers questions and plans edits through structured tools over that index — `profile`, `get_callers`, `backflow`, `trace_path`, `skim_source`, and ~30 more.
3. **Edit, gated.** Every write passes syntax and semantic checks against the real language parser — a broken parse auto-reverts. Every write that lands reports its blast radius: the changed symbol, its callers, its holders.
4. **Verify.** A focused, context-aware repro is generated against the exact change and run under a runtime tracer that records real argument values, real returns, real dispatch — plus the selectively relevant existing test cases that the same blast-radius analysis surfaces.

## Features

- **Three tiers of truth** — proven edges carry evidence; ambiguous calls keep their full candidate lists instead of a guess; runtime traces settle what static analysis can't.
- **Blind spots, declared** — every unresolved call is classified: a real library call, an in-repo call with recorded candidates, or an honest unknown carrying the ID the compiler supposed. Nothing is silently dropped.
- **Runtime tracer** — hooks every call during execution and overlays the observations back onto the static map.
- **Reasoning you can click** — the same map that drives the tools drives a live call graph beside the chat; when the agent names a function, that node lights up.
- **Persistent memory** — durable per-repo facts survive restarts; conventions learned once aren't re-derived every session.
- **Dual-engine: code + markup** — a separate index for HTML/CSS/DOM-JS with cascade resolution and selector specificity, including frontend embedded inside Python strings.
- **Model-agnostic** — Anthropic, OpenAI, or any compatible API; the agent can escalate itself to a larger model mid-task when a problem outgrows the one running it.

## Language support

**Python · JavaScript · TypeScript · Java · C# · C++ · C · Go · Rust · Ruby**

One compiler, ten languages; tree-sitter is the only real dependency, and each language is a grammar plugin. The map looks the same everywhere: symbols, call edges, data flow, references, inheritance.

**Honest limits:** depth varies by language. Python is the deepest — it's where the runtime tracer works and where parsing is strongest. A Go codebase gets the same structural map as a Python one, but not runtime traces. Execution is local-only, and the agent doesn't browse the web: everything it knows about a project comes from the project's own source.

## Getting started

- **In the browser** — paste any public GitHub repo at [benzi.fly.dev](https://benzi.fly.dev); no install.
- **In VS Code** — chat, graph, and edit inside the editor: [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=varianttech.benzi).

## Greenfielding examples

Apps Benzi has built from scratch in a single chat session live in [`BENZI_GREENFIELDING_EXAMPLES/`](BENZI_GREENFIELDING_EXAMPLES/) — starting with [StallionSwipe](BENZI_GREENFIELDING_EXAMPLES/horse_tinder/), a Tinder for horses ([live](https://benzi.fly.dev/horse_tinder)).
