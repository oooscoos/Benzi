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

<p align="center"><b>The codebase, compiled for the agent.</b></p>

<p align="center">
  <a href="<WEBSITE_URL>">Website</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev">Live demo</a> &nbsp;·&nbsp;
  <a href="<MARKETPLACE_URL>">VS&nbsp;Code&nbsp;Marketplace</a>
</p>

Benzi is a coding agent that actually **understands your codebase** — not by grepping or guessing, but by compiling it into a precise, queryable map: every symbol, call edge, and reference resolved up front. It navigates, reads, runs, and edits *through that map*, so it's **fast** (it never re-reads your whole repo) and **precise** (it reasons from proven structure, not vibes). It can even run your code to capture real runtime values, and it remembers what it learns from one session to the next.

<p align="center">
  <img src="https://raw.githubusercontent.com/shobhitx64/Benzi/main/assets/demo.gif" alt="Benzi in action" width="820">
</p>

## Try it in 30 seconds

- **Live demo — no install:** **[benzi.fly.dev](https://benzi.fly.dev)** — paste any public GitHub repo link and start asking.
- **VS Code extension:** **[install from the Marketplace](<MARKETPLACE_URL>)** — Benzi docks an interactive call-graph map + chat agent right next to your code.

## What makes it different

- **A resolved map, not a text search.** Benzi compiles your project once into an exact index — proven call edges, data flow, references — and queries *that* instead of re-reading files. Fewer tokens, sharper answers.
- **It runs your code.** Click a Python file's run button (or just ask) and Benzi traces the actual execution, capturing real argument and return values — the only truth for dynamic dispatch, callbacks, and anything a runtime decides.
- **Everything is verifiable.** When Benzi names a function, it lights up on the graph — click to jump straight to the source. Answers you can check, not take on faith.
- **Persistent memory.** What it learns about your codebase carries across sessions.

## Requirements

- **Python 3.9+** on your machine — the extension builds its own isolated environment on first run (nothing to configure).
- **No API key needed** — chat runs on the hosted Benzi service.

## Links

- 🌐 **Website** — <WEBSITE_URL>
- ▶️ **Live demo** — https://benzi.fly.dev
- 🧩 **VS Code Marketplace** — <MARKETPLACE_URL>

---

<p align="center"><sub>Built by <b>Variant</b>.</sub></p>
