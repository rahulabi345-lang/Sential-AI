from __future__ import annotations

import socket
from typing import Any

from data_security.api.public_interface import ingest_event


def collect_windows_event(event_data: dict[str, Any]) -> str:
    """
    Convert normalized Windows event data into a Sentinel-AI event.
    """

    required_fields = {
        "source",
        "event_type",
        "severity",
        "host",
        "description",
    }

    missing = required_fields - event_data.keys()

    if missing:
        raise ValueError(
            f"Missing required event fields: {sorted(missing)}"
        )

    return ingest_event(event_data)


def read_recent_windows_events(
    log_name: str = "System",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Read recent Windows Event Log records.

    Returns normalized dictionaries that can be passed to
    collect_windows_event().
    """

    import win32evtlog

    if limit <= 0:
        return []

    handle = win32evtlog.OpenEventLog("localhost", log_name)

    try:
        flags = (
            win32evtlog.EVENTLOG_BACKWARDS_READ
            | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        )

        records: list[dict[str, Any]] = []

        while len(records) < limit:
            events = win32evtlog.ReadEventLog(
                handle,
                flags,
                0,
            )

            if not events:
                break

            for event in events:
                records.append(
                    {
                        "source": "windows_event_log",
                        "event_type": str(event.EventID),
                        "severity": "info",
                        "host": socket.gethostname(),
                        "description": (
                            f"Windows Event ID {event.EventID} "
                            f"from {event.SourceName}."
                        ),
                        "raw_data": {
                            "event_id": event.EventID,
                            "source_name": event.SourceName,
                            "event_category": event.EventCategory,
                            "event_type": event.EventType,
                            "record_number": event.RecordNumber,
                            "time_generated": str(event.TimeGenerated),
                            "string_inserts": list(
                                event.StringInserts or []
                            ),
                            "data": (
                                event.Data.hex()
                                if event.Data
                                else ""
                            ),
                        },
                    }
                )

                if len(records) >= limit:
                    break

        return records

    finally:
        win32evtlog.CloseEventLog(handle)


def collect_recent_windows_events(
    log_name: str = "System",
    limit: int = 10,
) -> list[str]:
    """
    Read recent Windows events and store them in Sentinel-AI.
    """

    events = read_recent_windows_events(
        log_name=log_name,
        limit=limit,
    )

    event_ids: list[str] = []

    for event_data in events:
        event_id = collect_windows_event(event_data)
        event_ids.append(event_id)

    return event_ids
