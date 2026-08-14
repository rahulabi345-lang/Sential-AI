# Sentinel AI — Frontend

An AI-powered defensive cybersecurity assistant for Windows. This repository contains the **frontend only** — a security dashboard that helps non-technical users understand suspicious activity on their computer.

> See [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) for full project scope, constraints, and design guidelines. Read it before making changes — it's the source of truth for what this frontend is (and is not) meant to do.

## Stack

- React + Vite
- Tailwind CSS
- Recharts (charts)
- Lucide React (icons)

## Status

🚧 Hackathon prototype. Currently running on **mock data** — no backend integration yet. Mock data lives in a dedicated module so it can be swapped for real API calls later with minimal changes.

## Getting Started

```bash
npm install
npm run dev
```

## Project Structure

```
sentinel-frontend/
├── README.md
├── PROJECT_CONTEXT.md   # Project scope & constraints — read first
├── src/
│   ├── components/       # Dashboard, threat cards, charts, alerts, etc.
│   ├── data/             # Mock data (to be replaced by API responses)
│   └── ...
└── ...
```

## Scope Reminder

This frontend renders **defensive** security information only (dashboards, alerts, explanations, logs). It does not implement or include any offensive security functionality, malware, or credential-related tooling. See `PROJECT_CONTEXT.md` for the full list of constraints.
