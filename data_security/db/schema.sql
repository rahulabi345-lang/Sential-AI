PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS security_events (
    event_id      TEXT PRIMARY KEY,
    timestamp     TEXT NOT NULL,
    source        TEXT NOT NULL,
    event_type    TEXT NOT NULL,
    severity      TEXT NOT NULL
        CHECK (severity IN ('info', 'low', 'medium', 'high', 'critical')),
    host          TEXT NOT NULL,
    user          TEXT,
    process_name  TEXT,
    description   TEXT NOT NULL,
    raw_data      TEXT NOT NULL DEFAULT '{}',
    created_at    TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_security_events_timestamp
    ON security_events (timestamp);

CREATE INDEX IF NOT EXISTS idx_security_events_severity
    ON security_events (severity);

CREATE INDEX IF NOT EXISTS idx_security_events_host
    ON security_events (host);


CREATE TABLE IF NOT EXISTS threats (
    threat_id          TEXT PRIMARY KEY,
    related_event_ids  TEXT NOT NULL DEFAULT '[]',
    threat_type        TEXT NOT NULL,
    confidence_score   REAL NOT NULL
        CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    severity           TEXT NOT NULL
        CHECK (severity IN ('info', 'low', 'medium', 'high', 'critical')),
    description        TEXT NOT NULL,
    indicators         TEXT NOT NULL DEFAULT '{}',
    status             TEXT NOT NULL DEFAULT 'new'
        CHECK (status IN ('new', 'investigating', 'confirmed', 'dismissed')),
    detected_at        TEXT NOT NULL,
    created_at         TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_threats_detected_at
    ON threats (detected_at);

CREATE INDEX IF NOT EXISTS idx_threats_severity
    ON threats (severity);

CREATE INDEX IF NOT EXISTS idx_threats_status
    ON threats (status);


CREATE TABLE IF NOT EXISTS risk_assessments (
    assessment_id       TEXT PRIMARY KEY,
    scope               TEXT NOT NULL,
    risk_score          REAL NOT NULL
        CHECK (risk_score >= 0.0 AND risk_score <= 100.0),
    risk_level          TEXT NOT NULL
        CHECK (risk_level IN ('low', 'medium', 'high', 'critical')),
    related_threat_ids  TEXT NOT NULL DEFAULT '[]',
    summary             TEXT NOT NULL,
    assessed_at         TEXT NOT NULL,
    created_at          TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_risk_assessments_scope
    ON risk_assessments (scope);

CREATE INDEX IF NOT EXISTS idx_risk_assessments_assessed_at
    ON risk_assessments (assessed_at);