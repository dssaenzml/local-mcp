# local-mcp – Portfolio MCP Server

A minimal, self-contained python [MCP](https://github.com/modelcontextprotocol/python-sdk) playground you can run locally or inside Docker.

---

## ✨ Features

• FastMCP-based server with a few example tools and resources (notes, add, BMI).  
• Fully reproducible Python environment managed by [uv](https://docs.astral.sh/uv/).  
• One-command Docker image (multi-stage, slim final layer).  
• Ready to be opened in [Cursor](https://docs.cursor.com/welcome) – see `.cursor/mcp.json`.

---

## 📋 Prerequisites

1. **Python >= 3.12** – only needed if you intend to run without Docker.  
2. **uv >= 0.2.0** – a next-gen package manager that replaces both `pip` and `virtualenv`.

### Installing `uv`

The recommended way is via [pipx](https://pypa.github.io/pipx/):

```bash
# install pipx if you don't have it yet
python3 -m pip install --user pipx
pipx ensurepath

# install uv globally (isolated in its own venv)
pipx install uv
```

Alternatively you can use `pip` directly (less isolated):

```bash
python3 -m pip install --user uv
```

> ℹ️ `uv` works on Linux, macOS, and Windows. Homebrew users can also `brew install uv`. See the [uv docs](https://github.com/astral-sh/uv) for more options.

---

## ⚙️ Setting up the project

Clone the repo and install the runtime dependencies into a local virtual environment managed by `uv`:

```bash
# 1. Clone
git clone https://github.com/dssaenzml/local-mcp.git
cd local-mcp

# 2. Create a virtual-env (./.venv) and install deps
uv venv         # create .venv
uv sync         # install *production* deps from uv.lock

# 3. Activate the venv (optional – uv activates automatically when running commands)
source .venv/bin/activate
```

---

## 🚀 Running the MCP server in dev mode

With the environment ready, start the server via `uv` so it can hot-reload when code changes:

```bash
uv run --with mcp mcp dev src/local_mcp/server.py
```

Explanation:

* `uv run` – executes a command inside the virtual-env (no need to `source`).
* `--with mcp` – ensures `mcp` is on the same execution path.
* `mcp dev` – launches FastMCP in development mode (auto-reload, extra logging).
* `src/local_mcp/server.py` – the entry file for this repo.

You should see logs indicating the server is ready to accept MCP connections (Cursor will automatically connect if configured).

> **Inspector tip**  
> The dev server prints a full URL that already contains the session token—for example:
>
> ```
> http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>
> ```
> Simply open that link in your browser instead of copying the token manually.

---

## 🐳 Running with Docker (optional)

Build the image:

```bash
docker build -t local-mcp .
```

Run it (stdin transport, suitable for Cursor):

```bash
docker run --rm -i local-mcp
```

---

## 🖥️ Using with Cursor

Cursor uses `.cursor/mcp.json` to find and start servers. Two profiles are pre-defined:

```json
{
  "local-mcp": {
    "command": "/Path/to/your/project/.venv/bin/python",
    "args": ["/Path/to/your/project/src/local_mcp/server.py"]
  },
  "local-mcp-docker": {
    "command": "docker",
    "args": ["run", "--rm", "-i", "--init", "-e", "DOCKER_CONTAINER=true", "local-mcp"]
  }
}
```

Pick whichever profile you prefer (rename/remove the other) and hit "MCP: Restart server" inside Cursor.

---

## 📦 Creating / Updating the lock-file

Whenever you change `pyproject.toml`, regenerate a deterministic lock with:

```bash
uv pip compile --no-dev -o uv.lock
```

Commit both the updated `pyproject.toml` and `uv.lock`.

---

## 🤝 Contributing / License

This is a personal portfolio project. Licensed under the MIT License.
