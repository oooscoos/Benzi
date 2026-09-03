<!--
  NOTE: the VS Code Marketplace requires ABSOLUTE image URLs -- relative paths
  render on GitHub but break on the Marketplace page, so the raw GitHub URLs
  below are intentional.
-->
<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/icon.png" width="120" alt="Benzi">
</p>

<h1 align="center">Benzi<br><sub>by <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/variant_logo.png" width="16" alt=""> <b>Variant Technologies</b></sub></h1>

<p align="center"><b>An AI coding agent that doesn't read — it <i>queries</i>.</b></p>

<p align="center">Benzi is free to use — actively in development, a work in progress.</p>

<p align="center">
  <a href="https://benzi.fly.dev/horse_tinder">StallionSwipe&nbsp;demo</a> &nbsp;·&nbsp;
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

Every file parsed, imports resolved, class ancestry built, every identifier traced to its definition — before a single question is answered. Call flow and data flow are joined at every call site, so a bad value traces to its origin in one tool call. Claude Code greps; Cursor embeds; Aider maps signatures; Benzi resolves — and answers in O(1). Every language runs its own tree-sitter grammar into that same compiled map — ten so far, plus a second engine for markup (HTML, CSS, DOM-JS) — see [Language support](#language-support) below.

<p align="center">
  <a href="https://benzi.fly.dev"><img src="https://img.shields.io/badge/Try_the_Demo_(Any_Repo)-1E7A5C?style=for-the-badge" alt="Try the demo (any repo)"></a>
  <br><br>
  <a href="https://benzi.fly.dev/horse_tinder"><img src="https://img.shields.io/badge/See_What_Benzi_Can_Build-1E7A5C?style=for-the-badge" alt="See what Benzi can build"></a>
  <br><br>
  <a href="https://benzi.fly.dev/benchmark"><img src="https://img.shields.io/badge/Benchmarks_and_SWE_bench_Report-1E7A5C?style=for-the-badge" alt="Benchmarks and SWE-bench report"></a>
  <br><br>
  <a href="https://marketplace.visualstudio.com/items?itemName=varianttech.benzi"><img src="https://img.shields.io/badge/Get_Benzi_for_VS_Code-1E7A5C?style=for-the-badge" alt="Get Benzi for VS Code"></a>
  <br><br>
  <a href="https://benzi.fly.dev/about"><img src="https://img.shields.io/badge/Visit_the_Website-1E7A5C?style=for-the-badge" alt="Visit the website"></a>
  <br><br>
  <a href="https://benzi.fly.dev/?repo=https://github.com/oooscoos/Benzi"><img src="https://img.shields.io/badge/Watch_Benzi_Analyze_Itself-1E7A5C?style=for-the-badge" alt="Watch Benzi analyze itself"></a>
</p>

## SWE-bench Verified

The full SWE-bench Verified set — 500 real GitHub issues from twelve Python repositories — run end to end on **DeepSeek v4-flash**, one attempt per instance, graded by the official `swebench.harness.run_evaluation` inside its own per-instance Docker images, with network access to GitHub and PyPI blocked inside every container.

| | |
|---|---|
| **Resolved** | **391 / 500 — 78.2%** |
| Total cost, all 500 instances | $37.33 |
| Cost per instance resolved | $0.095 |
| Source lines read (total / median) | 231,574 / 379 |
| Model turns (total / median) | 16,091 / 27 |
| Input tokens served from cache | 97% |
| Output tokens | 22.0M |

Full technical report: [swebench/SWE_BENCH_REPORT.md](swebench/SWE_BENCH_REPORT.md) ([web version](https://benzi.fly.dev/report)). Every instance's cost, tokens, turns, and lines read: [benzi.fly.dev/benchmark_swebench](https://benzi.fly.dev/benchmark_swebench). The cross-harness efficiency comparison below (and the full 24-bug chart): [benzi.fly.dev/benchmark](https://benzi.fly.dev/benchmark).

## Live demos

**[StallionSwipe](BENZI_GREENFIELDING_EXAMPLES/horse_tinder/) · Python, HTML, CSS, JS** — a dating app for horses, greenfielded by Benzi from scratch in a single chat session. No image is a file: every horse portrait is procedural SVG, generated in code. Match with one and it flirts back through a real model, live. Frontend, backend, and the prompts — all written by Benzi. [Try it live](https://benzi.fly.dev/horse_tinder).

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht2.jpeg" width="200" alt="StallionSwipe swipe deck">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht4.jpeg" width="200" alt="StallionSwipe profile detail">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht3.jpeg" width="200" alt="StallionSwipe live AI chat">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht1.jpeg" width="200" alt="StallionSwipe profile creation">
</p>

**[VS Code's own source, resolved](https://benzi.fly.dev/about) · TypeScript** — the real `microsoft/vscode` repo is 1.8M lines; this indexes 923k of them: the editor core (`src/vs/editor` + `src/vs/base`), the platform services layer, and workbench's shell/API/browser plumbing — deliberately excluding the 747k-line grab-bag of individual features in `workbench/contrib`. Built once, in just over two minutes, then cached. [Try it live](https://benzi.fly.dev/about) (chat panel, near the bottom of the page).

**[Cool demo, watch Benzi analyze this Benzi repo itself](https://benzi.fly.dev/?repo=https://github.com/oooscoos/Benzi).**

**Or, try any repo of your choice at all here** — point Benzi at any public GitHub repo and it builds the index live. [benzi.fly.dev](https://benzi.fly.dev).

## Tools

A sample of 16 of Benzi's 35+ tools — what falls out of actually resolving the code, from the index itself to the gates on every write.

| Tool | What it answers |
|---|---|
| `get_callers` | Every call site that reaches a function — the code that will feel a change. |
| `call_tree` | The transitive call closure from one function, forward or in reverse. |
| `trace_path` | The call chain connecting two functions, and the data carried along it. |
| `external_calls` | Which libraries a scope leans on, and where it calls into them. |
| `forwardflow` | Where a function's return value ends up, everywhere it has to match. |
| `backflow` | Where a wrong value came from, without opening every caller. |
| `profile` | The full 360 on one symbol in a single call. |
| `get_definition` | The declaration card — signature, docs and location. |
| `search_symbols` | Case-insensitive substring search across every symbol in the repo. |
| `get_hierarchy` | A type's resolved bases and its direct subclasses. |
| `skim_source` | A body's one-level outline, so you know which lines are worth reading. |
| `execute_from` | Runs a file under the call tracer and records what actually happened. |
| `check_last_execution` | Reads back the last recorded run's facts, no re-run needed. |
| `execute_generated_testcase` | Writes a self-contained repro and runs it to debug its own change. |
| `rollback_edit` | Undoes the last writes by snapshot reload, not by re-editing. |
| `upgrade_to_pro` | Escalates itself to a larger reasoning budget mid-task. |

## How it works

1. **Compile.** Tree-sitter parses every file; imports are resolved, class ancestry built, every identifier traced to its definition. The output is an index, not a blob of text.
2. **Query.** The agent answers questions and plans edits through structured tools over that index — `profile`, `get_callers`, `backflow`, `trace_path`, `skim_source`, and ~30 more.
3. **Edit, gated.** Every write passes syntax and semantic gates against the real language parser — a broken parse auto-reverts. The model checks blast radius *before* it changes anything, not just after: the same analysis — the changed symbol, its callers, its holders, the selectively relevant existing tests — runs both going in and once a write lands.
4. **Verify.** A focused, context-aware repro is generated against the exact change and run under a runtime tracer that records real argument values, real returns, real dispatch — plus the selectively relevant existing test cases that the same blast-radius analysis surfaces.

## What the index actually changes

Same 24 bugs, one run each, four harness/model combinations. **Lines read** counts only what came back from file-read calls — grep and shell output are search, not reading, so this is the one figure that means the same thing in every harness.

| Harness · model | Lines read | vs Benzi |
|---|---:|---:|
| **Benzi · Sonnet** | **9,125** | — |
| Benzi · DeepSeek | 16,407 | 1.8× |
| Claude Code · Sonnet | 20,704 | 2.3× |
| DeepSeek Harness · DeepSeek | 43,598 | 4.8× |

Every harness opens more source as bugs get harder — the question is the slope. Benzi's stays flatter because it answers most of what a bug needs from the map instead of by reading.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_lines_read.png" width="600" alt="Source lines read per bug, all four harnesses">
</p>

Benzi reads the least source on every bug and the gap widens as bugs get harder — the index answers most of what a fix needs before a file is ever opened.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_wall_clock.png" width="600" alt="Wall-clock time per bug, all four harnesses">
</p>

Wall-clock time tracks close across all four — reading less doesn't make Benzi slower to think, just cheaper to look.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_cost.png" width="600" alt="Cost per fix, all four harnesses">
</p>

Benzi on DeepSeek costs about a cent a bug; Claude Code climbs to $0.18 a step as bugs get harder — roughly 18x.

More detail, per-bug breakdowns, and full methodology: [benzi.fly.dev/benchmark](https://benzi.fly.dev/benchmark).

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

Benzi is completely free to use.

- **In the browser** — paste any public GitHub repo at [benzi.fly.dev](https://benzi.fly.dev); no install, no signup. Read-only: ask it questions, explore the map, nothing writes to the repo. This is the demo — click here to see what it can do.
- **In VS Code** — the same compiler, but with edit access: chat, graph, and Benzi actually writing code in your own project. [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=varianttech.benzi). This is the real tool — click here to use it.

There's no headless or CLI mode (as of yet) — the browser and VS Code are the only two ways in.

## BONUS DEMO: Reading a real codebase: DOOM · C

Everyone says DOOM's engine was ahead of its time. Almost nobody has opened `z_zone.c` to see why. So we pointed Benzi at it. A few things were worth writing down.

**There is no `malloc()` during gameplay.** id (the developer) wrote their own memory allocator — one big arena grabbed once at startup, sliced into blocks tagged by how precious they are (`PU_STATIC`, `PU_LEVEL`, `PU_CACHE`...). The genius part: allocating new memory can silently evict old "cache" blocks it walks past along the way — no one calls `free()`, the allocator just decides your cached texture is cheap to regenerate and reclaims the space on the spot. That's cache-eviction policy baked directly into the allocation path itself. `malloc`/`free` still can't do that today.

**There's no floating point math, anywhere, in the renderer.** `tables.c` is a 2,000+ line file that is almost entirely one thing: every sine, tangent and arctangent value the engine will ever need, precomputed at compile time into lookup tables. Movement, angles, rendering — all fixed-point integer math against these tables. Not every '93 machine had an FPU, and even where it did, table lookups beat live trig every time.

**The whole screen is just a byte array — and "UI" isn't a system, it's a coincidence.** `screens[0]` is a flat 320×200 buffer, one byte per pixel. The 3D world gets drawn into it column by column. Then the HUD gets stamped on top using the exact same pixel-blitting function used to draw monster sprites and gun sprites. There is no UI toolkit, no widget tree, because there was nothing to build one on top of: the game owns the entire display, full stop. A health digit and a demon sprite are the same kind of draw call.

**Collision detection has its own hand-rolled spatial index.** `p_maputl.c` splits the map into a grid (the "blockmap") so hit detection only checks nearby geometry instead of scanning every wall in the level — a spatial hash, built from scratch, years before that was a common technique people talked about.

None of this was over-engineering. Every one of these systems exists because the standard answer (`malloc`, floats, a GUI library, brute-force collision) either didn't exist on the target hardware or would have been too slow.

*Explored with Benzi — an AI that reads codebases like this one directly, instead of guessing from memory.*
