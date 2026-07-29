<!--
  NOTE: the VS Code Marketplace requires ABSOLUTE image URLs -- relative paths
  render on GitHub but break on the Marketplace page. Once the public repo
  exists, replace shobhitx64/Benzi below with the real owner/name so the raw
  GitHub URLs resolve in both places.
-->
<p align="center">
  <img src="https://raw.githubusercontent.com/shobhitx64/Benzi/main/icon.png" width="120" alt="Benzi">
</p>

<h1 align="center">Benzi</h1>

<p align="center"><b>An AI coding agent that doesn't guess — it <i>reads</i>.</b></p>

<p align="center">
  <a href="https://benzi.fly.dev/about">Website</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev">Live demo</a> &nbsp;·&nbsp;
  <a href="<MARKETPLACE_URL>">VS&nbsp;Code&nbsp;Marketplace</a>
</p>

Every other agent dumps your files into a context window and hopes. Benzi compiles your codebase into a resolved map first — calls, data flow, references — then navigates it with real tools. One compiler, ten languages, one map.

<p align="center">
  <img src="https://raw.githubusercontent.com/shobhitx64/Benzi/main/assets/demo.gif" alt="Benzi in action" width="820">
</p>

## Try it in 30 seconds

- **Live demo — no install:** **[benzi.fly.dev](https://benzi.fly.dev)** — paste any public GitHub repo link and start asking.
- **VS Code extension:** **[install from the Marketplace](<MARKETPLACE_URL>)** — Benzi docks an interactive call-graph map + chat agent right next to your code.

## What makes it different

- **Compiled map, not a context dump.** Parallel parse every file, resolve imports, build class ancestry, trace every identifier to its definition — before answering a single question. A queryable index, not a blob of text.
- **Three tiers of truth.** Proven edges resolved with evidence. Candidate edges the compiler refuses to guess on. Observed edges from real runtime traces.
- **Runtime tracer.** Hooks every call at runtime — real argument values, real returns, real dispatch. Overlays onto the static map. No speculation.
- **Call flow + data flow, one join.** Who calls whom and where a value originates — indexed separately, joined at every call site. Trace a bad value to its origin in one tool call.
- **Context-aware runtime testcases.** Benzi writes a focused repro against the code you just changed, runs it under the real call tracer, and returns the observed values — no guesswork, no mock harness.
- **Syntax-gated edits + blast radius.** Every edit checked with the real language parser. Broken parse = auto revert. Every successful edit reports the changed symbol, its callers, its holders.
- **Persistent memory.** Durable per-repo facts survive restarts. Conventions and gotchas learned once aren't re-derived every session.
- **Model-agnostic.** Anthropic, OpenAI, or any compatible API. The intelligence lives in the tools and the map, not the model.
- **Dual-engine: code + markup.** A separate index for HTML/CSS/DOM-JS — cascade resolution, JS grabs, even frontend embedded inside Python strings.

## Language support

Python, JavaScript, TypeScript, Java, C#, C++, C, Go, Rust, Ruby — one compiler, one map. Tree-sitter is the only real dependency — everything else is just a grammar plugin.

## Requirements

- **Python 3.9+** on your machine — the extension builds its own isolated environment on first run (nothing to configure).
- **No API key needed** — chat runs on the hosted Benzi service.

## Links

- 🌐 **Website** — https://benzi.fly.dev/about
- ▶️ **Live demo** — https://benzi.fly.dev
- 📊 **Benchmark** — https://benzi.fly.dev/benchmark
- 🧩 **VS Code Marketplace** — <MARKETPLACE_URL>

---

(I, Benzi, wrote this doc too.)
