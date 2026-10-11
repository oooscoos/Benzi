<!--
  NOTE: the VS Code Marketplace requires ABSOLUTE image URLs -- relative paths
  render on GitHub but break on the Marketplace page, so the raw GitHub URLs
  below are intentional.
-->
<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/benzi_wordmark_raleway_400.png" width="140" alt="benzi">
</p>

<p align="center">Language Agnostic · Model Agnostic · Compiles Locally · BYOK · MCP Compatible</p>

<p align="center">
  <a href="https://pypi.org/project/benzi/"><img src="https://img.shields.io/pypi/v/benzi?color=97ca00&labelColor=000000&cacheSeconds=43200" alt="PyPI version" height="17"></a>
  <a href="https://pypi.org/project/benzi/"><img src="https://img.shields.io/pypi/pyversions/benzi?color=97ca00&labelColor=000000&cacheSeconds=86400" alt="Python versions" height="17"></a>
  <img src="https://img.shields.io/badge/MCP-compatible-97ca00?labelColor=000000" alt="MCP compatible" height="17">
  <a href="https://pepy.tech/projects/benzi"><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fvarianttech.net%2Fbadge%2Fdownloads.json&cacheSeconds=301" alt="Downloads (PyPI + VS Code)" height="17"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-proprietary-97ca00?labelColor=000000" alt="License" height="17"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/benzi_banner_v3.png" width="1000" alt="Benzi -- compiler-backed code intelligence">
</p>

<p align="center">
  <a href="https://varianttech.net/demo"><img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/cta2_demo.png" width="140" alt="Demo"></a>
  <br>
  <a href="#getting-started"><img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/cta2_download.png" width="149" alt="Download"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="#faq"><img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/cta2_faq.png" width="101" alt="FAQ"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://varianttech.net/benchmark"><img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/cta2_benchmarks.png" width="149" alt="Benchmarks"></a>
</p>

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

<div align="center">

### <u>Contents</u>

[What is Benzi](#what-is-benzi) — how it works in one paragraph
<br>[Live demos](#live-demos) — StallionSwipe, VS Code's own source, or any repo you paste
<br>[Language support](#language-support) — ten languages, and where the depth is uneven
<br>[Getting started](#getting-started) — the Benzi agent (VS Code or headless), or the compiler over MCP
<br>[What people say](#what-people-say) — what people wrote about it
<br>[SWE-bench Verified](#swe-bench-verified) — 391/500 (78.2%) for $37.33
<br>[How it works](#how-it-works) — compile, query, edit, verify
<br>[Tools](#tools) — 16 of the 35+ the index makes possible
<br>[What the index actually changes](#what-the-index-actually-changes) — lines read vs three other harnesses
<br>[Features](#features) — six states, runtime tracer, live call graph, memory, markup engine
<br>[FAQ & comparisons](#faq) — privacy, pricing, limits, and how Benzi compares

</div>

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>What is Benzi</u>

Most AI coding agents dump a repo into a context window and hope the model finds what matters. Benzi parses every file first — a real compiler, built on tree-sitter — into a precise, queryable map. Every symbol, every call edge, every reference, every class in its inheritance chain. One pass, done.

Every file parsed, imports resolved, class ancestry built, every identifier traced to its definition — before a single question is answered. Call flow and data flow join at every call site, so a bad value traces to its origin in one tool call. Claude Code greps; Cursor embeds; Aider maps signatures; Benzi resolves — in O(1). Ten languages so far, plus a markup engine for HTML, CSS, and DOM-JS — see [Language support](#language-support).

You can try pasting this repo's link to Benzi in the [live demo](https://varianttech.net/demo) too!

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/benzi_on_sqlite.png" width="900" alt="Benzi on SQLite">
  <br>
  <sub>Benzi on SQLite</sub>
</p>

<p align="center"><sub>Like where this is headed? A ⭐ goes a long way.</sub></p>

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>Live demos</u>

**[StallionSwipe](BENZI_GREENFIELDING_EXAMPLES/horse_tinder/) · Python, HTML, CSS, JS** — a dating app for horses, greenfielded by Benzi from scratch in a single chat session. No image is a file: every horse portrait is procedural SVG, generated in code. Match with one and it flirts back through a real model, live. Frontend, backend, and the prompts — all written by Benzi. [Try it live](https://varianttech.net/horse_tinder).

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht2.jpeg" width="200" alt="StallionSwipe swipe deck">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht4.jpeg" width="200" alt="StallionSwipe profile detail">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht3.jpeg" width="200" alt="StallionSwipe live AI chat">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/stallionswipe/ht1.jpeg" width="200" alt="StallionSwipe profile creation">
</p>

**[VS Code's own source, resolved](https://varianttech.net/about) · TypeScript** — the real `microsoft/vscode` repo is 1.8M lines; this indexes 923k of them: the editor core (`src/vs/editor` + `src/vs/base`), the platform services layer, and workbench's shell/API/browser plumbing — deliberately excluding the 747k-line grab-bag of individual features in `workbench/contrib`. Built once, in just over two minutes, then cached. [Try it live](https://varianttech.net/about) (chat panel, near the bottom of the page).

**Or, try any repo of your choice at all here** — point Benzi at any public GitHub repo and it builds the index live. [varianttech.net/demo](https://varianttech.net/demo).

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>Language support</u>

**Python · JavaScript · TypeScript · Java · C# · C++ · C · Go · Rust · Ruby**

One compiler, ten languages — each is a tree-sitter grammar plugin, so the core of the map (symbols, call edges, references, inheritance, data flow) is built the same way everywhere.

**Depth is uneven.** Python is deepest, and the only one with the runtime tracer. Every language reaches the core of the map, but each has its own constructs, not all modelled yet. For most code, every other language's map comes close to Python's.

Incremental reindexing is also less optimized for C, C++, Rust, and Ruby — it works, just not as fast on a large edit loop.

Wrong or thin answer in your language? [Open an issue](https://github.com/oooscoos/Benzi/issues) with the repo, the question, and what it got wrong — that's how the uneven parts get found.

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>Getting started</u>

Benzi is completely free to use during beta. There are two ways to use it, and they share one login: the same `benzi-login` config works everywhere.

1. **The Benzi agent** — Benzi's own agent, running on the compiled index, in VS Code or from the terminal. These features are part of the agent itself, so they come with VS Code and headless and are **not available over MCP**:

   - **Runtime tracer** — runs your code and records what actually happened: which target each ambiguous call really hit, with the real argument values.
   - **Static-analysis-gated edits** — every write is syntax-checked and checked against a fresh index before the next step; an edit that breaks the code is rolled back instead of built on.
   - **Blast radius before and after every edit** — who calls the symbol, who holds it, and what feeds its parameters, before the change and again once it lands.
   - **Self-aware upgrade to pro** — when a task outgrows the model it's running on, the agent upgrades itself to a larger model, then drops back when the task is done. Set `BENZI_ESCALATE_MODEL=deepseek-pro` (or another model alias) to turn it on.
   - **Persistent memory and rollback** — per-repo facts that survive restarts, and one-step undo of any edit.

   Run it either way:

   - **VS Code extension** — [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=varianttech.benzi)

     1. Install **Benzi** from the VS Code Marketplace.
     2. Click the **Benzi** icon in the left activity bar (circled below) to open the **Benzi: Settings** panel.
     3. Pick your model and paste your API key: an Anthropic key, or a non-Anthropic one (DeepSeek, Groq, Kimi and others).
     4. Enter your email and press **Send**, then type in the one-time code it emails you.
     5. Press **Save model & keys**, then **Run Benzi**.

     <p align="center">
       <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/benzi_login_settings.png" width="380" alt="The Benzi: Settings panel in VS Code">
     </p>

   - **Headless CLI** — [PyPI](https://pypi.org/project/benzi/)

     The same steps as the VS Code extension, from your terminal: install, log in, set your model and key, then run.

     ```bash
     pip install benzi
     ```

     Python 3.11–3.14 on Windows, macOS and Linux. Installs the `benzi-login`, `benzi-headless` and `benzi-mcp` commands.

     **1. Log in** — emails you a one-time code to type in.

     ```bash
     benzi-login --login you@example.com
     ```

     **2. Set your model and key**

     ```bash
     benzi-login --model deepseek
     benzi-login --nonanthropic-key YOUR_KEY      # or for Claude models: benzi-login --anthropic-key YOUR_KEY
     ```

     **3. Run it on a repo** — from the terminal, for scripts and CI.

     ```bash
     benzi-headless . "fix the failing test in parser.py"
     ```

2. **The Benzi compiler as an MCP server** — the compiled index, served as tools to the agent you already use: Claude Code, Cursor, or any MCP client. This is the map without Benzi's agent loop, so output quality depends on your agent, and the agent features above aren't included.

   The steps are the same as headless: `pip install benzi`, then log in with `benzi-login`. You can skip the model and key, because your own agent does the model calls. Then register `benzi-mcp` with your agent instead of running `benzi-headless`. For example, in Claude Code, once for all your projects:

   ```bash
   claude mcp add --scope user benzi -- benzi-mcp
   ```

   `benzi-mcp` then serves whichever folder you start Claude Code in, so switching projects needs nothing extra. To pin it to one repo no matter where you start, pass that repo's path:

   ```bash
   claude mcp add --scope user benzi -- benzi-mcp /path/to/your/repo
   ```

VS Code's settings panel and `benzi-login` share one config: log in once, and VS Code, headless and MCP all use it.

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>What people say</u>

> "78.2% for $37 is a slap in the face to the 'brute force wins' school."
> — Alex Xiang, [**zicode**](https://zicode.com/blog/ai-coding-supply-chain/) *(translated)*

> "Benzi is proving that the core competency of coding tools is shifting from simple 'reading comprehension' to 'structural grasping ability.'"
> — Gi Pyeong Lee, [**Tech Blog**](https://gipyeong-lee.github.io/2026/09/11/Show-HN-Benzi-A-Code-IntillegenceHarness-Beating-Claude-Code-and-CodeGraph.en/)

> "Fewer tokens, no context drift. Wild idea, honestly."
> — [**prompt 🤖 AI News**](https://t.me/prompt/392)

> "It analyzes changes before writing them — and beats Claude Code on benchmarks."
> — [**Ponte al dIA**](https://ponte-al-dia.com/p/benzi-agente-de-codigo-que-supera-a-claude-sonnet-en-tareas-de-programacion) *(translated)*

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>SWE-bench Verified</u>

The full SWE-bench Verified set — 500 real GitHub issues from twelve Python repositories — run end to end on **DeepSeek v4-flash**, one attempt per instance, graded by the official `swebench.harness.run_evaluation` inside its own per-instance Docker images, with network access to GitHub and PyPI blocked inside every container.

<div align="center">

| | |
|:---:|:---:|
| **Resolved** | **391 / 500 — 78.2%** |
| Total cost, all 500 instances | $37.33 |
| Cost per instance resolved | $0.095 |
| Source lines read (total / median) | 231,574 / 379 |
| Model turns (total / median) | 16,091 / 27 |
| Input tokens served from cache | 97% |
| Output tokens | 22.0M |

</div>

Full technical report: [swebench/SWE_BENCH_REPORT.md](swebench/SWE_BENCH_REPORT.md) ([web version](https://varianttech.net/report)). Every instance's cost, tokens, turns, and lines read: [varianttech.net/benchmark_swebench](https://varianttech.net/benchmark_swebench). The cross-harness efficiency comparison below (and the full 24-bug chart): [varianttech.net/benchmark](https://varianttech.net/benchmark).

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>How it works</u>

1. **Compile.** Tree-sitter parses every file, resolves imports, builds class ancestry, traces every identifier to its definition. Output is an index, not text.
2. **Query.** The agent reads and plans through structured tools over that index — `profile`, `get_callers`, `backflow`, `trace_path`, `skim_source`, ~30 more.
3. **Edit, gated.** Every write is checked against the real parser; a broken parse auto-reverts. Blast radius — the changed symbol, its callers, its holders, the relevant tests — is checked going in and again once the write lands.
4. **Verify by running it.** A focused repro runs under a runtime tracer alongside the tests blast-radius flagged. Real values, real dispatch: this proves the change and settles the map — ambiguous edges collapse onto whatever target actually fired.
5. **Reindex, incrementally.** Every turn re-parses only what changed on disk — your edits and the agent's, treated the same.
6. **Revert, from a snapshot.** Every write snapshots the index first, so undo reloads that snapshot instead of re-deriving it.
7. **Back to step 2.** The next question always answers against the code as it is now.

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>Tools</u>

A sample of 16 of Benzi's 35+ tools — what falls out of actually resolving the code, from the index itself to the gates on every write.

<div align="center">

| Tool | What it answers |
|:---:|:---:|
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

</div>

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>What the index actually changes</u>

Same 24 bugs, one run each, four harness/model combinations. **Lines read** counts only what came back from file-read calls — grep and shell output are search, not reading, so this is the one figure that means the same thing in every harness.

<div align="center">

| Harness · model | Lines read | vs Benzi |
|:---:|:---:|:---:|
| **Benzi · Sonnet** | **9,125** | — |
| Benzi · DeepSeek | 16,407 | 1.8× |
| Claude Code · Sonnet | 20,704 | 2.3× |
| DeepSeek Harness · DeepSeek | 43,598 | 4.8× |

</div>

Every harness opens more source as bugs get harder — the question is the slope. Benzi's stays flatter because it answers most of what a bug needs from the map instead of by reading.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_lines_read.png" width="780" alt="Source lines read per bug, all four harnesses">
</p>

Benzi reads the least source on every bug and the gap widens as bugs get harder — the index answers most of what a fix needs before a file is ever opened.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_wall_clock.png" width="780" alt="Wall-clock time per bug, all four harnesses">
</p>

Wall-clock time tracks close across all four — reading less doesn't make Benzi slower to think, just cheaper to look.

<p align="center">
  <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/chart_cost.png" width="780" alt="Cost per fix, all four harnesses">
</p>

Benzi on DeepSeek costs about a cent a bug; Claude Code climbs to $0.18 a step as bugs get harder — roughly 18x.

More detail, per-bug breakdowns, and full methodology: [varianttech.net/benchmark](https://varianttech.net/benchmark).

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

### <u>Features</u>

- **Six states, never a guess** — every call site and every file carries one: **resolved** (proven in-repo edge), **external** (into a library, with the import evidence), **candidate** (ambiguous — the bounded set of possible targets, kept in full), **unresolved** (seen but not settled, carrying *why*), **observed** (confirmed by an actual run), **unindexed** (never parsed, with the reason). One rule throughout: whatever static analysis can't settle is flagged as unsettled rather than guessed — and running the program is what settles it.
- **Runtime tracer** — hooks every call during execution and overlays the observations back onto the static map.
- **Reasoning you can click** — the same map that drives the tools drives a live call graph beside the chat; when the agent names a function, that node lights up.
- **Persistent memory** — durable per-repo facts survive restarts; conventions learned once aren't re-derived every session.
- **Dual-engine: code + markup** — a separate index for HTML/CSS/DOM-JS with cascade resolution and selector specificity, including frontend embedded inside Python strings.
- **Model-agnostic** — Anthropic, OpenAI, or any compatible API; the agent can escalate itself to a larger model mid-task when a problem outgrows the one running it.

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

<a name="faq"></a>

### <u>FAQ & comparisons</u>

**Does my code leave my machine?**
No. In VS Code, the CLI, or MCP, the compiler and index run locally — nothing uploaded, no copy kept. Only the snippets the agent actually reads go to your model provider, same as any AI assistant, and less of them: **9,125** lines read vs Claude Code's 20,704 on the same 24 bugs. The browser demo differs — it fetches a *public* repo server-side, read-only, deletes it after your session.

**Is it actually free?**
Yes, Benzi doesn't charge. The CLI and MCP are BYOK, so you pay your own model provider. Early and in development — that's the trade, not a paywall.

**Can it run on a local model?**
In principle, yes: Benzi talks to models through standard APIs, so a local model (Ollama, LM Studio and the like) could plug in. It isn't supported yet, though. Today Benzi runs on hosted providers with your own key.

**Can I point it at a private repo?**
Not the web demo (public GitHub API only). Everywhere else, yes — the compiler runs locally on whatever path you give it.

**How large a repo can it handle?**
VS Code handles real codebases — `microsoft/vscode`, 923k lines, indexes in ~2 minutes, then caches. The browser demo caps at 2,000 files, 2 MB each.

**How is this different from Cursor, Copilot, or Claude Code?**
They search — grep or embeddings. Benzi resolves first: a real index of symbols, calls, inheritance, data flow, queried instead of guessed. Same 24 bugs, 2.3× less source read than Claude Code. Details: [what the index actually changes](#what-the-index-actually-changes).

**How is this different from an LSP-backed MCP server?**
An LSP answers at a cursor, in one open file: go-to-definition or find-references, one position and one hop at a time. Benzi compiles the whole repo up front into one index, so the questions are whole-codebase ones: transitive call trees, the path between two functions, and **data flow**, meaning where a bad value came from or where a return value lands. Every answer also carries a **confidence tier**: resolved, candidate, unresolved (with the reason), or observed. An LSP gives an answer or nothing. The **runtime tracer** then settles what static analysis can't by watching what actually fires. And the compiler itself is **language agnostic**: ten languages run through one pipeline into one index format. An LSP setup needs a separate server per language, each installed, configured and kept running.

**How is this different from CodeQL or Sourcegraph's SCIP indexers?**
They need a working build and index in batch: dependencies installed, the project compiling, a CI job measured in minutes. Benzi needs no build, works on half-finished code, and re-parses only what changed on every turn. That's what makes gated writes possible: each edit is checked against a fresh index before the next step, not after a rebuild. One pipeline covers all ten languages instead of one indexer per language. Where that costs precision, Benzi flags the call site as candidate or unresolved instead of guessing.

**How is this different from CodeGraph?**
Both index instead of search, but CodeGraph **retrieves** — ranked candidates from a queried database. Benzi **resolves** — settles what a name binds to before answering, and refuses rather than guesses when a call site is ambiguous. It also models code the way an engineer reads it — file → scopes → call flow → data/control flow — not a flat symbol graph.

On CodeGraph's own benchmark (their repos, their questions, their methodology), Gemini, ChatGPT, Claude and DeepSeek each reviewed the answers from a fresh account, and all four ranked Benzi's first. Full results: [varianttech.net/benchmark_codegraph](https://varianttech.net/benchmark_codegraph).

<img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/assets/divider_gold.png" width="100%" alt="">

<p align="center"><sub>by <img src="https://raw.githubusercontent.com/oooscoos/Benzi/main/icons/variant_logo_circle.png" width="16" alt=""> <b>Variant Technologies</b></sub></p>
