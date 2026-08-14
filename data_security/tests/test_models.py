import pytest
from pydantic import ValidationError

from data_security.models.security_event import SecurityEvent, Severity


def _valid_event_kwargs():
    return {
        "source": "windows_event_log",
        "event_type": "process_start",
        "severity": Severity.MEDIUM,
        "host": "DESKTOP-01",
        "description": "Suspicious process started.",
        "raw_data": {
            "pid": 1234,
            "path": "C:\\Windows\\System32\\notepad.exe",
        },
    }


def test_valid_security_event_is_constructed():
    event = SecurityEvent(**_valid_event_kwargs())

    assert event.host == "DESKTOP-01"
    assert event.severity == Severity.MEDIUM
    assert event.event_id
    assert event.timestamp is not None
    assert event.created_at is not None
    assert event.raw_data["pid"] == 1234


def test_invalid_severity_is_rejected():
    kwargs = _valid_event_kwargs()
    kwargs["severity"] = "super_critical"

    with pytest.raises(ValidationError):
        SecurityEvent(**kwargs)


def test_description_over_max_length_is_rejected():
    kwargs = _valid_event_kwargs()
    kwargs["description"] = "x" * 2001

    with pytest.raises(ValidationError):
        SecurityEvent(**kwargs)


def test_description_at_max_length_is_accepted():
    kwargs = _valid_event_kwargs()
    kwargs["description"] = "x" * 2000

    event = SecurityEvent(**kwargs)

    assert len(event.description) == 2000


def test_empty_description_is_rejected():
    kwargs = _valid_event_kwargs()
    kwargs["description"] = "   "

    with pytest.raises(ValidationError):
        SecurityEvent(**kwargs)