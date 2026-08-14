import { levelFromScore } from '../constants/severity';

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    throw new Error(`API error ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

function formatTimestamp(isoString) {
  if (!isoString) return '';
  return new Date(isoString).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}

// --- Dashboard (GET /stats -> StatsResponse) -------------------------------
// The backend gives counts per severity (low/medium/high/critical) rather
// than one 0-100 risk score, so we compute a severity-weighted score here.
// This is OUR heuristic, not something the backend sends — worth confirming
// with the backend teammate if a different formula was intended.
function computeRiskScore(stats) {
  const { low = 0, medium = 0, high = 0, critical = 0, total_events = 0 } = stats;
  if (total_events === 0) return 0;
  const weighted = low * 1 + medium * 2 + high * 3 + critical * 4;
  const maxPossible = total_events * 4;
  return Math.round((weighted / maxPossible) * 100);
}

export async function getDashboard() {
  const s = await request('/stats');
  const riskScore = computeRiskScore(s);
  const riskLevel = levelFromScore(riskScore);
  const isProtected = riskLevel === 'LOW';

  return {
    status: isProtected ? 'protected' : 'at_risk',
    statusLabel: isProtected ? 'System Protected' : 'System At Risk',
    riskScore,
    riskLevel,
    riskTrend: 0, // backend doesn't provide a trend yet — defaults safely
    threatCount: s.total_alerts ?? 0,
    eventCount24h: s.total_events ?? 0,
    criticalAlerts: s.critical ?? 0,
    lastScan: s.latest_event_timestamp ? formatTimestamp(s.latest_event_timestamp) : 'just now',
  };
}

// --- Recent Threats (GET /alerts -> AlertResponse[]) ------------------------
// AlertResponse only contains HIGH/CRITICAL events, no "title" field — using
// event_type as the card title since that's the closest match.
function adaptAlert(a) {
  const severity = (a.risk_level ?? levelFromScore(a.risk_score ?? 80)).toLowerCase();
  return {
    id: a.event_id,
    severity,
    title: a.event_type,
    description: a.ai_summary ?? 'No summary available yet.',
    process: a.process_name,
    timestamp: formatTimestamp(a.timestamp),
  };
}

export async function getThreats() {
  const data = await request('/alerts');
  return data.map(adaptAlert);
}

// --- Full event log (GET /events -> SecurityEventResponse[]) ---------------
// For the Events page (not wired up yet) — richer than alerts, includes
// every event regardless of severity, with AI fields already attached.
function adaptEvent(e) {
  const severity = (e.risk_level ?? levelFromScore(e.risk_score ?? 0)).toLowerCase();
  return {
    id: e.id,
    severity,
    title: e.ai_title || e.event_type,
    description: e.ai_summary || e.description,
    process: e.process_name,
    timestamp: formatTimestamp(e.timestamp),
  };
}

export async function getEvents() {
  const data = await request('/events');
  return data.map(adaptEvent);
}

// --- AI Analysis (POST /events/{event_id}/analyze -> AIAnalysisResponse) ---
export async function getThreatAnalysis(eventId) {
  const data = await request(`/events/${eventId}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return {
    summary: data.summary,
    whySuspicious: data.indicators ?? [],
    recommendation: (data.recommended_actions ?? []).join(' '),
  };
}