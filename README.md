# Agent Analytics MCP Server 📊

Usage analytics and monitoring for AI agent tool calls. Track, analyze, and optimize how agents use your tools.

## Features

- **Event Tracking** — Log every tool call with duration, success/failure, metadata
- **Dashboard** — Overview with total calls, error rates, top tools, daily trends
- **Per-Tool Analytics** — Deep dive into individual tool performance
- **Per-Agent Analytics** — See how specific agents use your services
- **Error Tracking** — Monitor and debug failures

## Installation

```bash
pip install agent-analytics-mcp-server
```

## Usage with Claude Code

```json
{
  "mcpServers": {
    "analytics": {
      "command": "uvx",
      "args": ["agent-analytics-mcp-server"]
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `track_event` | Log a usage event |
| `get_dashboard` | Overview dashboard |
| `tool_analytics` | Per-tool deep dive |
| `agent_analytics` | Per-agent usage |

## License

MIT
