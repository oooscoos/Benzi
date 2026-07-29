# Single-user codebase-explorer webapp, containerized for Fly.io (one
# Fly Machine per visitor session -- see fly.toml). No build step, no node
# toolchain: explorer.py's pages are self-contained HTML strings, so the
# only real dependency is tree-sitter-language-pack's compiled grammars.
FROM python:3.12-slim

# tree-sitter-language-pack ships prebuilt wheels for linux/amd64 + arm64,
# so no compiler toolchain is needed here -- keep the image lean.
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# tracer.py, editor.py, webanchor.py, memory.py all ship because agentchat
# top-imports the four -- the image crashes at import without them (exactly
# what happened when webanchor/memory were added to agentchat's imports but
# not to this list). Hosted, the execution tools stay dead (no session gets a
# run_config), but editing is now LIVE -- webapp sets edit_config on the
# throwaway per-session download -- and the markup/memory tools work against
# that same disposable session dir.
COPY codemap2.py languages.py explorer.py webapp.py mobile.py hierarchy_view.py ir_parser.py agentchat.py graph.py tracer.py editor.py webanchor.py memory.py frontend_hierarchy.py frontend_graph.py frontend_agentchat.py public_sans_font.py overpass_font.py benchmark.html benzi_landing.html favicon.png ./

# Fly Machines route HTTP in from outside the container -- must bind all
# interfaces, and there's no browser/display inside the container to open.
ENV HOST=0.0.0.0
EXPOSE 8765

# DEEPSEEK_API_KEY (or whichever provider's key --chat-model needs) is
# supplied at deploy time via `fly secrets set`, never baked into the image.
CMD ["python", "webapp.py", "--host", "0.0.0.0", "--port", "8765", "--no-browser", "--chat-model", "deepseek"]
