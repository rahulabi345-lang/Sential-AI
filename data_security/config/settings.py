from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


MODULE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = MODULE_ROOT / "db" / "sentinel.db"


@dataclass(frozen=True)
class Settings:
    db_path: str
    max_description_length: int
    event_query_default_limit: int
    event_query_max_limit: int
    log_level: str

    @property
    def db_path_obj(self) -> Path:
        return Path(self.db_path)


def get_settings() -> Settings:
    return Settings(
        db_path=os.getenv(
            "SENTINEL_DB_PATH",
            str(DEFAULT_DB_PATH),
        ),
        max_description_length=int(
            os.getenv(
                "SENTINEL_MAX_DESCRIPTION_LENGTH",
                "2000",
            )
        ),
        event_query_default_limit=int(
            os.getenv(
                "SENTINEL_EVENT_QUERY_DEFAULT_LIMIT",
                "50",
            )
        ),
        event_query_max_limit=int(
            os.getenv(
                "SENTINEL_EVENT_QUERY_MAX_LIMIT",
                "500",
            )
        ),
        log_level=os.getenv(
            "SENTINEL_LOG_LEVEL",
            "INFO",
        ),
    )