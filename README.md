# Sentinel-AI

AI-powered cybersecurity assistant for Windows.

## Overview

Sentinel-AI is a cybersecurity data and risk management system designed to collect security events, identify threats, and store risk assessments.

The current implementation provides:

- Security event validation and storage
- Threat validation and storage
- Risk assessment validation and storage
- SQLite database persistence
- Repository-based data access
- A public Python API
- Automated tests

## Project Structure

```text
Sential-AI/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
└── data_security/
    ├── __init__.py
    │
    ├── api/
    │   ├── __init__.py
    │   └── public_interface.py
    │
    ├── config/
    │   ├── __init__.py
    │   └── settings.py
    │
    ├── db/
    │   ├── __init__.py
    │   ├── connection.py
    │   └── schema.sql
    │
    ├── models/
    │   ├── __init__.py
    │   ├── security_event.py
    │   ├── threat.py
    │   └── risk_assessment.py
    │
    ├── repository/
    │   ├── __init__.py
    │   ├── event_repository.py
    │   ├── threat_repository.py
    │   └── risk_repository.py
    │
    ├── schemas/
    │   ├── __init__.py
    │   ├── event_schema.py
    │   └── threat_schema.py
    │
    └── tests/
        ├── __init__.py
        ├── test_api.py
        ├── test_models.py
        ├── test_repository.py
        └── test_validation.py
