"""Analytics-Tools — Usage-Tracking und Monitoring für AI-Agents."""

from mcp.server.fastmcp import FastMCP

from src import db


def register_analytics_tools(mcp: FastMCP):
    """Analytics-bezogene MCP-Tools registrieren."""

    @mcp.tool()
    async def track_event(
        event_type: str,
        tool_name: str = None,
        service_id: str = "default",
        agent_id: str = None,
        duration_ms: int = None,
        success: bool = True,
        error_message: str = None,
        metadata: dict = None,
    ) -> dict:
        """Ein Usage-Event tracken.

        Zeichnet einen Tool-Aufruf oder ein anderes Event auf
        für spätere Analyse.

        Args:
            event_type: Art des Events (z.B. "tool_call", "error", "login")
            tool_name: Name des aufgerufenen Tools
            service_id: ID des Services (Standard: "default")
            agent_id: ID des aufrufenden Agents
            duration_ms: Dauer in Millisekunden
            success: War der Aufruf erfolgreich?
            error_message: Fehlermeldung falls nicht erfolgreich
            metadata: Zusätzliche Daten als JSON
        """
        return db.track_event(
            event_type, tool_name, service_id,
            agent_id, duration_ms, success, error_message, metadata,
        )

    @mcp.tool()
    async def get_dashboard(service_id: str = None, days: int = 30) -> dict:
        """Analytics-Dashboard abrufen.

        Zeigt: Gesamtaufrufe, Erfolgsrate, Top-Tools, tägliche Nutzung.

        Args:
            service_id: Optional — nur für diesen Service
            days: Zeitraum in Tagen (Standard: 30)
        """
        return db.get_dashboard(service_id, days)

    @mcp.tool()
    async def tool_analytics(tool_name: str, days: int = 30) -> dict:
        """Detaillierte Analytics für ein spezifisches Tool.

        Zeigt: Aufrufe, Erfolgsrate, Durchschnittsdauer,
        letzte Fehler und täglichen Trend.

        Args:
            tool_name: Name des Tools
            days: Zeitraum in Tagen (Standard: 30)
        """
        return db.get_tool_analytics(tool_name, days)

    @mcp.tool()
    async def agent_analytics(agent_id: str, days: int = 30) -> dict:
        """Analytics für einen bestimmten Agent.

        Zeigt welche Tools ein Agent wie oft nutzt.

        Args:
            agent_id: ID des Agents
            days: Zeitraum in Tagen (Standard: 30)
        """
        return db.get_agent_analytics(agent_id, days)
