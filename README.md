# web-mcp

MCP server that fetches web content using a browser user agent. Provides two tools:

- **`fetch_raw`** — returns the raw HTML/text of a URL
- **`fetch_text`** — returns extracted readable text (strips scripts, styles, and HTML tags)

## Install

```bash
python -m venv .venv
.venv/bin/pip install -e .
```

## Usage

### Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "web-mcp": {
      "command": "/path/to/.venv/bin/web-mcp"
    }
  }
}
```

### CLI

```bash
.venv/bin/web-mcp
```

## Tests

```bash
.venv/bin/pip install pytest pytest-cov pytest-asyncio
.venv/bin/pytest -v
```

Coverage is enforced at 100% by default.
