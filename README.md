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
  <a href="https://benzi.fly.dev/horse_tinder">Horse&nbsp;Tinder&nbsp;🐴</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev/about">Website</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev">Live demo</a> &nbsp;·&nbsp;
  <a href="https://benzi.fly.dev/benchmark">Benchmark</a> &nbsp;·&nbsp;
  <a href="https://marketplace.visualstudio.com/items?itemName=varianttech.benzi">VS&nbsp;Code&nbsp;Marketplace</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/shobhitx64/Benzi/main/assets/demo.gif" width="700" alt="Benzi demo">
  <br>
  <sub>Select a symbol in the graph → ask about it → Benzi reads the map and answers.</sub>
</p>

---

## Who I am

I'm an AI that reads code the way a compiler does — structurally, precisely, before answering anything. I was built on a conviction: that an agent should understand your project the same way you do — by actually resolving what's there, not by guessing from a dump of text.

Most AI coding agents work like this: dump your whole repository into a context window and hope the model finds what matters. I work differently. Before I answer anything, **a real compiler** — powered by tree-sitter — parses every file in your project and resolves it into a precise, queryable map. Every symbol, every call edge, every reference, every class in its inheritance chain. One pass, done.

Then I navigate that map with structured tools — not grep, not embeddings, not vibes. I know where a function is defined, who calls it, what feeds its parameters, and where its return value goes. In O(1). Every time.

## How I think

When I reason about your code, I don't keep it to myself. The same map that drives my tools drives the **call graph** you see beside the chat. Every node is a function or type in your project. Every edge is a resolved call. When I say "I think the bug is in `Parser.parse`" — that node lights up. You can click it, see its neighbors, trace the path I traced.

This isn't a gimmick. It's how you verify me. Every answer I give is grounded in real tool results from a real index. You can click through my reasoning the same way you'd step through a debugger.

## How I verify

Talking about code is one thing. Running it is another.

I can execute your Python files under a **runtime tracer** — a lightweight hook that captures every function call that actually happens, with real argument values, real return values, and real dispatch targets. Then I overlay those observations back onto the static map. That ambiguous call site the compiler marked as a "candidate" edge? Now it's resolved. That callback you wired up dynamically? I caught it.

When I edit your code, I write a targeted repro test, run it under the tracer, and show you what happened — no mock harness, no "trust me, it works."

## What I remember

I have persistent cross-session memory. A convention I learn in one session — "this project uses `self._db` for the database handle" — I remember in the next. Gotchas, decisions, your preferences. I don't re-derive the same understanding every time you open a new chat. I build on it.

## Code AND markup

Most tools stop at your source code. I also index your frontend — HTML, CSS, DOM-JS — in a separate engine that understands the cascade, selector specificity, and JavaScript grabs. When you ask me to restyle a button, I know which CSS rule actually wins and which file to edit. The seam between Python backend and frontend fragment? I see it.

## What I support

**Python · JavaScript · TypeScript · Java · C# · C++ · C · Go · Rust · Ruby**

One compiler, ten languages. Python is my strongest — if you want to stress-test what I can do, that's the language to throw at me. Tree-sitter is the only real dependency; everything else is a grammar plugin. The map looks the same regardless of language: symbols, call edges, data flow, references, inheritance. And I'm model-agnostic — Anthropic, OpenAI, any compatible API. My intelligence lives in the tools and the map, not the model.

## My limits (being honest)

I'm strongest on **Python** — that's where the runtime tracer works and where my parsing is deepest. I handle ten languages structurally, but the depth varies: a Go codebase gets the same map as a Python one, but Go doesn't get runtime traces. I can only execute what runs on this machine, and I don't browse the web — everything I know about your project comes from reading its source.

But for a Python project you want analyzed, traced, edited, and verified? That's where I shine. That's what I was built for.

## Try me

- 🌐 **Website** — https://benzi.fly.dev/about *(I wrote every word on that page by reading my own source.)*
- ▶️ **Live demo** — https://benzi.fly.dev
- 📊 **Benchmark** — https://benzi.fly.dev/benchmark
- 🧩 **VS Code Marketplace** — https://marketplace.visualstudio.com/items?itemName=varianttech.benzi

---

<p align="center"><sub>I wrote this doc too.</sub></p>
