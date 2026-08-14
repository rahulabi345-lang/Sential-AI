from __future__ import annotations

import json
import sqlite3
from typing import Any, Optional

from data_security.models.security_event import SecurityEvent, Severity


class EventRepository:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db_path = db_path

    def _conn(self):
        from data_security.db.connection import get_connection

        return get_connection(self._db_path)

    def add_event(self, event: SecurityEvent) -> str:
        """Insert a validated SecurityEvent and return its ID."""

        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO security_events (
                    event_id,
                    timestamp,
                    source,
                    event_type,
                    severity,
                    host,
                    user,
                    process_name,
                    description,
                    raw_data,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.timestamp.isoformat(),
                    event.source,
                    event.event_type,
                    event.severity.value,
                    event.host,
                    event.user,
                    event.process_name,
                    event.description,
                    json.dumps(event.raw_data),
                    event.created_at.isoformat(),
                ),
            )

        return event.event_id

    def get_event(
        self,
        event_id: str,
    ) -> Optional[SecurityEvent]:

        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM security_events
                WHERE event_id = ?
                """,
                (event_id,),
            ).fetchone()

        return self._row_to_model(row) if row else None

    def query_events(
        self,
        *,
        severity: Optional[Severity] = None,
        host: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[SecurityEvent]:

        clauses: list[str] = []
        params: list[Any] = []

        if severity is not None:
            clauses.append("severity = ?")
            params.append(severity.value)

        if host is not None:
            clauses.append("host = ?")
            params.append(host)

        if source is not None:
            clauses.append("source = ?")
            params.append(source)

        where_sql = (
            f"WHERE {' AND '.join(clauses)}"
            if clauses
            else ""
        )

        params.extend([limit, offset])

        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT *
                FROM security_events
                {where_sql}
                ORDER BY timestamp DESC
                LIMIT ?
                OFFSET ?
                """,
                params,
            ).fetchall()

        return [
            self._row_to_model(row)
            for row in rows
        ]

    @staticmethod
    def _row_to_model(
        row: sqlite3.Row,
    ) -> SecurityEvent:

        return SecurityEvent(
            event_id=row["event_id"],
            timestamp=row["timestamp"],
            source=row["source"],
            event_type=row["event_type"],
            severity=Severity(row["severity"]),
            host=row["host"],
            user=row["user"],
            process_name=row["process_name"],
            description=row["description"],
            raw_data=json.loads(row["raw_data"]),
            created_at=row["created_at"],
        )