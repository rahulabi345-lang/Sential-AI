import sys
from types import SimpleNamespace

import data_security.collectors.windows_event_collector as collector


def test_read_recent_windows_events_preserves_event_details(monkeypatch):
    fake_event = SimpleNamespace(
        EventID=19,
        SourceName="Microsoft-Windows-WindowsUpdateClient",
        EventCategory=1,
        EventType=4,
        RecordNumber=29587,
        TimeGenerated="2026-08-13 08:54:31",
        StringInserts=(
            "Security Intelligence Update for Microsoft Defender Antivirus",
            "{ea2948a4-b36a-4535-acb5-2979cb65a3a4}",
            "200",
        ),
        Data=b"",
    )

    class FakeWin32EvtLog:
        EVENTLOG_BACKWARDS_READ = 1
        EVENTLOG_SEQUENTIAL_READ = 2

        @staticmethod
        def OpenEventLog(server, log_name):
            return "fake-handle"

        @staticmethod
        def ReadEventLog(handle, flags, offset):
            return [fake_event]

        @staticmethod
        def CloseEventLog(handle):
            pass

    monkeypatch.setitem(
        sys.modules,
        "win32evtlog",
        FakeWin32EvtLog,
    )

    events = collector.read_recent_windows_events(
        log_name="System",
        limit=1,
    )

    assert len(events) == 1

    event = events[0]

    assert event["event_type"] == "19"
    assert event["severity"] == "info"
    assert event["raw_data"]["event_id"] == 19
    assert (
        event["raw_data"]["source_name"]
        == "Microsoft-Windows-WindowsUpdateClient"
    )
    assert event["raw_data"]["string_inserts"] == [
        "Security Intelligence Update for Microsoft Defender Antivirus",
        "{ea2948a4-b36a-4535-acb5-2979cb65a3a4}",
        "200",
    ]
