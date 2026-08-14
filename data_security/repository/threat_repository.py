from __future__ import annotations

import json
import sqlite3
from typing import Any, Optional

from data_security.models.security_event import Severity
from data_security.models.threat import Threat, ThreatStatus


class ThreatRepository:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db_path = db_path

    def _conn(self):
        from data_security.db.connection import get_connection

        return get_connection(self._db_path)

    def add_threat(self, threat: Threat) -> str:
        """Insert a validated Threat and return its ID."""

        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO threats (
                    threat_id,
                    related_event_ids,
                    threat_type,
                    confidence_score,
                    severity,
                    description,
                    indicators,
                    status,
                    detected_at,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    threat.threat_id,
                    json.dumps(threat.related_event_ids),
                    threat.threat_type,
                    threat.confidence_score,
                    threat.severity.value,
                    threat.description,
                    json.dumps(threat.indicators),
                    threat.status.value,
                    threat.detected_at.isoformat(),
                    threat.created_at.isoformat(),
                ),
            )

        return threat.threat_id

    def get_threat(
        self,
        threat_id: str,
    ) -> Optional[Threat]:

        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM threats
                WHERE threat_id = ?
                """,
                (threat_id,),
            ).fetchone()

        return self._row_to_model(row) if row else None

    def query_threats(
        self,
        *,
        severity: Optional[Severity] = None,
        status: Optional[ThreatStatus] = None,
        threat_type: Optional[str] = None,
        host: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Threat]:

        clauses: list[str] = []
        params: list[Any] = []

        if severity is not None:
            clauses.append("t.severity = ?")
            params.append(severity.value)

        if status is not None:
            clauses.append("t.status = ?")
            params.append(status.value)

        if threat_type is not None:
            clauses.append("t.threat_type = ?")
            params.append(threat_type)

        if host is not None:
            clauses.append(
                """
                EXISTS (
                    SELECT 1
                    FROM security_events e
                    WHERE e.host = ?
                    AND EXISTS (
                        SELECT 1
                        FROM json_each(t.related_event_ids) related
                        WHERE related.value = e.event_id
                    )
                )
                """
            )
            params.append(host)

        where_sql = (
            f"WHERE {' AND '.join(clauses)}"
            if clauses
            else ""
        )

        params.extend([limit, offset])

        with self._conn() as conn:
            rows = conn.execute(
                f"""
                SELECT t.*
                FROM threats t
                {where_sql}
                ORDER BY t.detected_at DESC
                LIMIT ?
                OFFSET ?
                """,
                params,
            ).fetchall()

        return [
            self._row_to_model(row)
            for row in rows
        ]

    def update_status(
        self,
        threat_id: str,
        status: ThreatStatus,
    ) -> bool:

        with self._conn() as conn:
            cursor = conn.execute(
                """
                UPDATE threats
                SET status = ?
                WHERE threat_id = ?
                """,
                (status.value, threat_id),
            )

        return cursor.rowcount > 0

    @staticmethod
    def _row_to_model(
        row: sqlite3.Row,
    ) -> Threat:

        return Threat(
            threat_id=row["threat_id"],
            related_event_ids=json.loads(
                row["related_event_ids"]
            ),
            threat_type=row["threat_type"],
            confidence_score=row["confidence_score"],
            severity=Severity(row["severity"]),
            description=row["description"],
            indicators=json.loads(
                row["indicators"]
            ),
            status=ThreatStatus(row["status"]),
            detected_at=row["detected_at"],
            created_at=row["created_at"],
        )