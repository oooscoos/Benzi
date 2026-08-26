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

The agent then navigates that map with structured tools. Claude Code searches with grep. Cursor searches with embeddings. Aider reads tree-sitter signatures. Benzi resolves the full structure ahead of time, so where a function is defined, who calls it, what feeds its parameters, and where its return value ends up are each one O(1) lookup, every time — not a search.

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

## What the index actually changes

Same 24 bugs, one run each, four harness/model combinations. **Lines read** counts only what came back from file-read calls — grep and shell output are search, not reading, so this is the one figure that means the same thing in every harness.

| Harness · model | Lines read | vs Benzi |
|---|---:|---:|
| **Benzi · Sonnet** | **9,125** | — |
| Benzi · DeepSeek | 16,407 | 1.8× |
| Claude Code · Sonnet | 20,704 | 2.3× |
| DeepSeek Harness · DeepSeek | 43,598 | 4.8× |

Every harness opens more source as bugs get harder — the question is the slope. Benzi's stays flatter because it answers most of what a bug needs from the map instead of by reading.

## Live demos

**[StallionSwipe](BENZI_GREENFIELDING_EXAMPLES/horse_tinder/)** — a dating app for horses, greenfielded by Benzi from scratch in a single chat session. No image is a file: every horse portrait is procedural SVG, generated in code. Match with one and it flirts back through a real model, live. Frontend, backend, and the prompts — all written by Benzi. [Try it live](https://benzi.fly.dev/horse_tinder).

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht2.jpeg" width="200" alt="StallionSwipe swipe deck">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht4.jpeg" width="200" alt="StallionSwipe profile detail">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht3.jpeg" width="200" alt="StallionSwipe live AI chat">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht1.jpeg" width="200" alt="StallionSwipe profile creation">
</p>

**[VS Code's own source, resolved](https://benzi.fly.dev/about)** — the real `microsoft/vscode` repo is 1.8M lines; this indexes 923k of them: the editor core (`src/vs/editor` + `src/vs/base`), the platform services layer, and workbench's shell/API/browser plumbing — deliberately excluding the 747k-line grab-bag of individual features in `workbench/contrib`. Built once, in just over two minutes, then cached. [Try it live](https://benzi.fly.dev/about) (chat panel, near the bottom of the page).

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

## Reading a real codebase: DOOM

Everyone says DOOM's engine was ahead of its time. Almost nobody has opened `z_zone.c` to see why. So we pointed Benzi at it. A few things were worth writing down.

**There is no `malloc()` during gameplay.** id (the developer) wrote their own memory allocator — one big arena grabbed once at startup, sliced into blocks tagged by how precious they are (`PU_STATIC`, `PU_LEVEL`, `PU_CACHE`...). The genius part: allocating new memory can silently evict old "cache" blocks it walks past along the way — no one calls `free()`, the allocator just decides your cached texture is cheap to regenerate and reclaims the space on the spot. That's cache-eviction policy baked directly into the allocation path itself. `malloc`/`free` still can't do that today.

**There's no floating point math, anywhere, in the renderer.** `tables.c` is a 2,000+ line file that is almost entirely one thing: every sine, tangent and arctangent value the engine will ever need, precomputed at compile time into lookup tables. Movement, angles, rendering — all fixed-point integer math against these tables. Not every '93 machine had an FPU, and even where it did, table lookups beat live trig every time.

**The whole screen is just a byte array — and "UI" isn't a system, it's a coincidence.** `screens[0]` is a flat 320×200 buffer, one byte per pixel. The 3D world gets drawn into it column by column. Then the HUD gets stamped on top using the exact same pixel-blitting function used to draw monster sprites and gun sprites. There is no UI toolkit, no widget tree, because there was nothing to build one on top of: the game owns the entire display, full stop. A health digit and a demon sprite are the same kind of draw call.

**Collision detection has its own hand-rolled spatial index.** `p_maputl.c` splits the map into a grid (the "blockmap") so hit detection only checks nearby geometry instead of scanning every wall in the level — a spatial hash, built from scratch, years before that was a common technique people talked about.

None of this was over-engineering. Every one of these systems exists because the standard answer (`malloc`, floats, a GUI library, brute-force collision) either didn't exist on the target hardware or would have been too slow.

*Explored with Benzi — an AI that reads codebases like this one directly, instead of guessing from memory.*
