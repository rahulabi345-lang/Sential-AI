from __future__ import annotations

import json
import sqlite3
from typing import Any, Optional

from data_security.models.risk_assessment import RiskAssessment, RiskLevel


class RiskRepository:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db_path = db_path

    def _conn(self):
        from data_security.db.connection import get_connection

        return get_connection(self._db_path)

    def add_assessment(self, assessment: RiskAssessment) -> str:
        """Insert a validated RiskAssessment and return its ID."""

        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO risk_assessments (
                    assessment_id,
                    scope,
                    risk_score,
                    risk_level,
                    related_threat_ids,
                    summary,
                    assessed_at,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    assessment.assessment_id,
                    assessment.scope,
                    assessment.risk_score,
                    assessment.risk_level.value,
                    json.dumps(assessment.related_threat_ids),
                    assessment.summary,
                    assessment.assessed_at.isoformat(),
                    assessment.created_at.isoformat(),
                ),
            )

        return assessment.assessment_id

    def get_latest_assessment(
        self,
        scope: str,
    ) -> Optional[RiskAssessment]:

        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM risk_assessments
                WHERE scope = ?
                ORDER BY assessed_at DESC
                LIMIT 1
                """,
                (scope,),
            ).fetchone()

        return self._row_to_model(row) if row else None

    def query_assessments(
        self,
        *,
        scope: Optional[str] = None,
        risk_level: Optional[RiskLevel] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[RiskAssessment]:

        clauses: list[str] = []
        params: list[Any] = []

        if scope is not None:
            clauses.append("scope = ?")
            params.append(scope)

        if risk_level is not None:
            clauses.append("risk_level = ?")
            params.append(risk_level.value)

        if start_time is not None:
            clauses.append("assessed_at >= ?")
            params.append(start_time)

        if end_time is not None:
            clauses.append("assessed_at <= ?")
            params.append(end_time)

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
                FROM risk_assessments
                {where_sql}
                ORDER BY assessed_at DESC
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
    ) -> RiskAssessment:

        return RiskAssessment(
            assessment_id=row["assessment_id"],
            scope=row["scope"],
            risk_score=row["risk_score"],
            risk_level=RiskLevel(row["risk_level"]),
            related_threat_ids=json.loads(
                row["related_threat_ids"]
            ),
            summary=row["summary"],
            assessed_at=row["assessed_at"],
            created_at=row["created_at"],
        )