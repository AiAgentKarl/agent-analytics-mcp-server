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


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
