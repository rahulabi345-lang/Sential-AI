from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

from data_security.config.settings import get_settings


_SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _connect(db_path: str) -> sqlite3.Connection:
    Path(db_path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


def initialize_database(
    db_path: Optional[str] = None,
) -> None:
    """Create the Sentinel AI database tables if they do not exist."""

    resolved_path = (
        db_path or get_settings().db_path
    )

    schema_sql = _SCHEMA_PATH.read_text(
        encoding="utf-8"
    )

    conn = _connect(resolved_path)

    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


@contextmanager
def get_connection(
    db_path: Optional[str] = None,
) -> Iterator[sqlite3.Connection]:
    """
    Open a SQLite connection.

    The connection commits automatically when successful
    and rolls back if an error occurs.
    """

    resolved_path = (
        db_path or get_settings().db_path
    )

    conn = _connect(resolved_path)

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()