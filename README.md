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

### Claude Code

```bash
claude mcp add web-mcp /path/to/web-mcp/.venv/bin/web-mcp
```

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "web-mcp": {
      "command": "/path/to/web-mcp/.venv/bin/web-mcp"
    }
  }
}
```

## Port

The default port for SSE/streamable-http transport is `9678`.

## Tests

```bash
.venv/bin/pip install -e ".[test]"
.venv/bin/pytest -v
```

Coverage is enforced at 100% by default.
