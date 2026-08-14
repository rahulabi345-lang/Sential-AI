# SENTINEL AI FRONTEND

Sentinel AI is an AI-powered defensive cybersecurity assistant for Windows.

Purpose:
Help users understand suspicious activity on their computer.

Frontend responsibility:
- Security dashboard
- Threat cards
- Risk indicators
- Security charts
- Security status
- Alert interface
- AI threat explanations
- Event logs

The application must NOT contain:
- Malware
- Credential theft
- Exploitation
- Unauthorized access
- Persistence mechanisms
- Offensive security functionality

Design:
- Modern cybersecurity/SOC dashboard
- Dark theme
- Professional
- Clean
- Responsive
- Easy for a non-technical user to understand

Important:
This is a hackathon prototype.
Prioritize working functionality and visual polish over unnecessary complexity.

Frontend stack:
React + Vite
Tailwind CSS
Recharts
Lucide React

Backend data will eventually come from APIs.
Until backend integration is ready, use mock data.

Frontend must be designed so mock data can easily be replaced with API responses.

This prevents your AI coding tool from repeatedly misunderstanding the project.

Build order:
1. App layout
2. Sidebar
3. Dashboard
4. Threat cards
5. Risk visualization
6. Activity charts
7. Threat details
8. Events page
9. AI explanation panel
10. Notifications
11. Backend API integration
12. Loading/error states
13. Final polish

Target folder structure:
src/
│
├── components/
│   ├── Sidebar.jsx
│   ├── Topbar.jsx
│   ├── RiskScore.jsx
│   ├── ThreatCard.jsx
│   ├── SecurityStatus.jsx
│   ├── ActivityChart.jsx
│   ├── EventTable.jsx
│   ├── AIExplanation.jsx
│   └── LoadingSpinner.jsx
│
├── pages/
│   ├── Dashboard.jsx
│   ├── Threats.jsx
│   ├── Events.jsx
│   ├── Reports.jsx
│   └── Settings.jsx
│
├── services/
│   └── api.js
│
├── data/
│   └── mockData.js
│
├── App.jsx
├── main.jsx
└── index.css
