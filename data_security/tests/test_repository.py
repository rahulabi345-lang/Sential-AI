import pytest

from data_security.db.connection import initialize_database
from data_security.models.risk_assessment import RiskAssessment, RiskLevel
from data_security.models.security_event import SecurityEvent, Severity
from data_security.models.threat import Threat, ThreatStatus
from data_security.repository.event_repository import EventRepository
from data_security.repository.risk_repository import RiskRepository
from data_security.repository.threat_repository import ThreatRepository


@pytest.fixture()
def db_path(tmp_path):
    path = str(tmp_path / "test_sentinel.db")
    initialize_database(path)
    return path


def test_event_insertion_and_retrieval(db_path):
    repo = EventRepository(db_path=db_path)

    event = SecurityEvent(
        source="windows_event_log",
        event_type="login_attempt",
        severity=Severity.LOW,
        host="DESKTOP-02",
        user="alice",
        description="A user logged in.",
        raw_data={"logon_type": 2},
    )

    event_id = repo.add_event(event)
    fetched = repo.get_event(event_id)

    assert fetched is not None
    assert fetched.event_id == event_id
    assert fetched.host == "DESKTOP-02"
    assert fetched.severity == Severity.LOW
    assert fetched.raw_data == {"logon_type": 2}

    results = repo.query_events(host="DESKTOP-02", limit=10)

    assert any(e.event_id == event_id for e in results)


def test_threat_insertion_and_retrieval(db_path):
    event_repo = EventRepository(db_path=db_path)
    threat_repo = ThreatRepository(db_path=db_path)

    event_id = event_repo.add_event(
        SecurityEvent(
            source="process_monitor",
            event_type="process_start",
            severity=Severity.HIGH,
            host="DESKTOP-03",
            description="Unusual process started.",
        )
    )

    threat = Threat(
        related_event_ids=[event_id],
        threat_type="suspicious_process",
        confidence_score=0.9,
        severity=Severity.HIGH,
        description="Process matches known suspicious pattern.",
        status=ThreatStatus.NEW,
    )

    threat_id = threat_repo.add_threat(threat)
    fetched = threat_repo.get_threat(threat_id)

    assert fetched is not None
    assert fetched.threat_id == threat_id
    assert fetched.related_event_ids == [event_id]
    assert fetched.confidence_score == pytest.approx(0.9)

    updated = threat_repo.update_status(
        threat_id,
        ThreatStatus.CONFIRMED,
    )

    assert updated is True

    refetched = threat_repo.get_threat(threat_id)

    assert refetched is not None
    assert refetched.status == ThreatStatus.CONFIRMED

    results = threat_repo.query_threats(
        status=ThreatStatus.CONFIRMED,
        limit=10,
    )

    assert any(t.threat_id == threat_id for t in results)


def test_risk_assessment_insertion_and_retrieval(db_path):
    risk_repo = RiskRepository(db_path=db_path)

    assessment = RiskAssessment(
        scope="system",
        risk_score=67.5,
        risk_level=RiskLevel.HIGH,
        summary="Multiple active threats detected.",
    )

    assessment_id = risk_repo.add_assessment(assessment)

    latest = risk_repo.get_latest_assessment("system")

    assert latest is not None
    assert latest.assessment_id == assessment_id
    assert latest.risk_score == pytest.approx(67.5)
    assert latest.risk_level == RiskLevel.HIGH

    history = risk_repo.query_assessments(
        scope="system",
        limit=10,
    )

    assert any(
        a.assessment_id == assessment_id
        for a in history
    )