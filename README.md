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

Benzi is an AI coding agent paired with a real compiler. The compiler parses your project with tree-sitter and resolves every symbol, call edge, and data flow into a queryable map — before the agent answers a single question. There's no context dump, no "hope this is relevant." Just a precise index the agent navigates with real tools.

When the agent reasons about your code, that thinking lights up on the call graph beside you. Every node and edge is clickable, every answer traceable back to real source. Run a Python file and the tracer captures actual runtime values — arguments, returns, dispatch — and feeds them back into the map. Dynamic calls that static analysis couldn't settle get resolved by what actually ran.

The compiler and the agent share the same index. You share it too. One compiler, ten languages (tree-sitter is the only real dependency), one map.

<p align="center">
  <img src="https://raw.githubusercontent.com/shobhitx64/Benzi/main/assets/demo.gif" alt="Benzi in action" width="820">
</p>

## Links

- 🌐 **Website** — https://benzi.fly.dev/about *(I built this page.)*
- ▶️ **Live demo** — https://benzi.fly.dev
- 📊 **Benchmark** — https://benzi.fly.dev/benchmark
- 🧩 **VS Code Marketplace** — <MARKETPLACE_URL>

---

<p align="center"><sub>(I, Benzi, wrote this doc too.)</sub></p>
