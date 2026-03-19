"""Datenbank — SQLite-basiertes Analytics-Tracking."""

import sqlite3
import json
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path


_DB_PATH = os.getenv("ANALYTICS_DB_PATH", str(Path(__file__).resolve().parent.parent / "analytics.db"))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            tool_name TEXT,
            service_id TEXT DEFAULT 'default',
            agent_id TEXT,
            duration_ms INTEGER,
            success INTEGER DEFAULT 1,
            error_message TEXT,
            metadata TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_event_type ON events(event_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tool ON events(tool_name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created ON events(created_at)")
    conn.commit()
    return conn


def track_event(
    event_type: str,
    tool_name: str = None,
    service_id: str = "default",
    agent_id: str = None,
    duration_ms: int = None,
    success: bool = True,
    error_message: str = None,
    metadata: dict = None,
) -> dict:
    """Event tracken."""
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """INSERT INTO events
           (event_type, tool_name, service_id, agent_id,
            duration_ms, success, error_message, metadata, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (event_type, tool_name, service_id, agent_id,
         duration_ms, 1 if success else 0, error_message,
         json.dumps(metadata) if metadata else None, now),
    )
    conn.commit()
    conn.close()
    return {"tracked": True, "event_type": event_type, "created_at": now}


def get_dashboard(service_id: str = None, days: int = 30) -> dict:
    """Dashboard-Daten abrufen."""
    conn = _connect()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    sql_where = "WHERE created_at >= ?"
    params = [cutoff]
    if service_id:
        sql_where += " AND service_id=?"
        params.append(service_id)

    # Gesamtstatistiken
    total = conn.execute(f"SELECT COUNT(*) as c FROM events {sql_where}", params).fetchone()["c"]
    successful = conn.execute(
        f"SELECT COUNT(*) as c FROM events {sql_where} AND success=1", params
    ).fetchone()["c"]
    failed = total - successful

    # Top Tools
    top_tools = conn.execute(
        f"""SELECT tool_name, COUNT(*) as calls, AVG(duration_ms) as avg_duration
            FROM events {sql_where} AND tool_name IS NOT NULL
            GROUP BY tool_name ORDER BY calls DESC LIMIT 10""",
        params,
    ).fetchall()

    # Tägliche Nutzung
    daily = conn.execute(
        f"""SELECT DATE(created_at) as date, COUNT(*) as calls
            FROM events {sql_where}
            GROUP BY DATE(created_at) ORDER BY date DESC LIMIT {days}""",
        params,
    ).fetchall()

    # Error-Rate
    error_rate = (failed / total * 100) if total > 0 else 0

    conn.close()
    return {
        "period_days": days,
        "total_events": total,
        "successful": successful,
        "failed": failed,
        "error_rate_pct": round(error_rate, 1),
        "top_tools": [dict(r) for r in top_tools],
        "daily_usage": [dict(r) for r in daily],
    }


def get_tool_analytics(tool_name: str, days: int = 30) -> dict:
    """Analytics für ein spezifisches Tool."""
    conn = _connect()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    rows = conn.execute(
        """SELECT COUNT(*) as calls,
                  SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) as successes,
                  AVG(duration_ms) as avg_duration_ms,
                  MIN(duration_ms) as min_duration_ms,
                  MAX(duration_ms) as max_duration_ms
           FROM events WHERE tool_name=? AND created_at >= ?""",
        (tool_name, cutoff),
    ).fetchone()

    # Letzte Fehler
    errors = conn.execute(
        """SELECT error_message, created_at FROM events
           WHERE tool_name=? AND success=0 AND created_at >= ?
           ORDER BY created_at DESC LIMIT 5""",
        (tool_name, cutoff),
    ).fetchall()

    # Täglicher Trend
    daily = conn.execute(
        """SELECT DATE(created_at) as date, COUNT(*) as calls
           FROM events WHERE tool_name=? AND created_at >= ?
           GROUP BY DATE(created_at) ORDER BY date""",
        (tool_name, cutoff),
    ).fetchall()

    conn.close()
    return {
        "tool_name": tool_name,
        "period_days": days,
        "total_calls": rows["calls"],
        "success_rate_pct": round(rows["successes"] / rows["calls"] * 100, 1) if rows["calls"] > 0 else 0,
        "avg_duration_ms": round(rows["avg_duration_ms"] or 0),
        "min_duration_ms": rows["min_duration_ms"],
        "max_duration_ms": rows["max_duration_ms"],
        "recent_errors": [dict(r) for r in errors],
        "daily_trend": [dict(r) for r in daily],
    }


def get_agent_analytics(agent_id: str, days: int = 30) -> dict:
    """Analytics für einen spezifischen Agent."""
    conn = _connect()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    tools_used = conn.execute(
        """SELECT tool_name, COUNT(*) as calls
           FROM events WHERE agent_id=? AND created_at >= ? AND tool_name IS NOT NULL
           GROUP BY tool_name ORDER BY calls DESC""",
        (agent_id, cutoff),
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) as c FROM events WHERE agent_id=? AND created_at >= ?",
        (agent_id, cutoff),
    ).fetchone()["c"]

    conn.close()
    return {
        "agent_id": agent_id,
        "total_events": total,
        "tools_used": [dict(r) for r in tools_used],
    }
