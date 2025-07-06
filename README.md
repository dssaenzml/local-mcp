# local-mcp – Portfolio MCP Server

A fully-featured python [MCP](https://github.com/modelcontextprotocol/python-sdk) server with multiple transport options, comprehensive tools, and Docker support.

---

## ✨ Features

• **Multiple Transport Options**: Supports both stdio and SSE (Server-Sent Events) transports  
• **Comprehensive Tool Set**: Notes management, calculations, and more  
• **Resource & Prompt Support**: Rich MCP capabilities with resources and prompts  
• **CLI Interface**: Easy command-line configuration with Click  
• **FastMCP-based server** with professional-grade architecture  
• **Fully reproducible Python environment** managed by [uv](https://docs.astral.sh/uv/)  
• **One-command Docker image** (multi-stage, slim final layer)  
• **Ready to be opened in [Cursor](https://docs.cursor.com/welcome)** – see `.cursor/mcp.json`

---

## 🛠️ Available Tools

The server provides several useful tools:

- **Notes Management**:
  - `add-note`: Create or overwrite notes with content
  - `list-notes`: List all available notes
  - `delete-note`: Remove notes from the server
  - `get-note-content`: Retrieve specific note content

- **Calculations**:
  - `add`: Simple addition of two numbers
  - `calculate-bmi`: BMI calculator (weight in kg, height in meters)

- **Resources**: Access notes via `note://{name}` resource URIs
- **Prompts**: `summarize-notes` prompt with optional detailed style

---

## 📋 Prerequisites

1. **Python >= 3.12** – only needed if you intend to run without Docker  
2. **uv >= 0.2.0** – a next-gen package manager that replaces both `pip` and `virtualenv`

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

# Note: After installation, the `local-mcp` CLI command becomes available
```

---

## 🚀 Running the MCP server

### Option 1: Standard stdio transport (for Cursor/Claude Desktop)

```bash
local-mcp
```

Or with explicit transport option:

```bash
local-mcp --transport stdio
```

### Option 2: SSE transport (for web-based integrations)

For Server-Sent Events transport, which is useful for web-based chat assistants:

```bash
local-mcp --transport sse --port 8000
```

This starts the server on `http://localhost:8000/sse` and you can use this URL in your chat assistant's MCP configuration.

### Development mode with hot-reload

For development with auto-reload on code changes (uses stdio transport):

```bash
mcp dev src/local_mcp/server.py
```

> **Inspector tip**  
> The dev server prints a full URL that already contains the session token—for example:
>
> ```
> http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<token>
> ```
> Simply open that link in your browser instead of copying the token manually.

### Quick Reference

| Mode | Command | Use Case |
|------|---------|----------|
| Stdio (default) | `local-mcp` | Cursor/Claude Desktop integration |
| SSE | `local-mcp --transport sse --port 8000` | Web-based chat assistants |
| Development | `mcp dev src/local_mcp/server.py` | Development with hot-reload |

---

## 🐳 Running with Docker

Build the image:

```bash
docker build -t local-mcp .
```

Run with stdio transport (suitable for Cursor):

```bash
docker run --rm -i local-mcp
```

Run with SSE transport:

```bash
docker run --rm -p 8000:8000 local-mcp --transport http
```

---

## 🖥️ Using with Cursor

Cursor uses `.cursor/mcp.json` to find and start servers. Three profiles are pre-defined:

```json
{
  "mcpServers": {
    "local-mcp": {
      "command": "/path/to/your/local-mcp/.venv/bin/python",
      "args": ["/path/to/your/local-mcp/src/local_mcp/server.py"]
    },
    "local-mcp-sse": {
      "url": "http://localhost:8000/mcp"
    },
    "local-mcp-docker": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "--init", "-e", "DOCKER_CONTAINER=true", "local-mcp"]
    }
  }
}
```

### Using stdio transport (default)
Use the `local-mcp` or `local-mcp-docker` profile. Update the paths to match your system:
- Replace `/path/to/your/local-mcp/` with your actual project path
- The command should point to `.venv/bin/python` in your project directory

### Using SSE transport
1. Start the server with SSE transport: `local-mcp --transport sse --port 8000`
2. Use the `local-mcp-sse` profile in Cursor
3. Hit "MCP: Restart server" inside Cursor

---

## 🔧 Command Line Options

The server supports the following CLI options:

```bash
local-mcp --help
```

- `--transport [stdio|sse]`: Choose transport method (default: stdio)
- `--port INTEGER`: Port to listen on for SSE transport (default: 8000)

---

## 📦 Creating / Updating the lock-file

Whenever you change `pyproject.toml`, regenerate a deterministic lock with:

```bash
uv lock
```

Commit both the updated `pyproject.toml` and `uv.lock`.

---

## 🔍 Testing the Server

You can test the tools using the MCP inspector or by integrating with compatible clients:

### Example: Adding a note
```bash
# The add-note tool will create a new note
# Parameters: name (string), content (string)
```

### Example: Calculating BMI
```bash
# The calculate-bmi tool calculates BMI
# Parameters: weight_kg (float), height_m (float)
```

---

## 🤝 Contributing / License

This is a personal portfolio project. Licensed under the MIT License.
