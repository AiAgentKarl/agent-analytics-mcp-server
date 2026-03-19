"""Agent Analytics MCP Server — Usage-Tracking für AI-Agent-Tools."""

from mcp.server.fastmcp import FastMCP

from src.tools.analytics import register_analytics_tools

mcp = FastMCP(
    "Agent Analytics",
    instructions=(
        "Track and analyze AI agent tool usage. Monitor call frequency, "
        "success rates, response times, and errors. "
        "Get dashboards and per-tool analytics."
    ),
)

register_analytics_tools(mcp)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
