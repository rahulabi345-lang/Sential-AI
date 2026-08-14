// Single source of truth for threat/risk severity across the whole app.
// Every component that shows a severity level (RiskScore, ThreatCard,
// and later the Events page / filters) should import from here instead
// of defining its own map — that's what keeps the language consistent
// as the app grows.
//
// Canonical levels — use only these four, nothing else:
export const SEVERITY = {
  LOW: {
    level: 'LOW',
    label: 'LOW RISK',
    color: '#34D399', // raw hex — used for SVG strokes/glows that Tailwind classes can't reach
    dot: 'bg-safe',
    text: 'text-safe',
    ring: 'ring-safe/25',
  },
  MEDIUM: {
    level: 'MEDIUM',
    label: 'MEDIUM RISK',
    color: '#F4C542',
    dot: 'bg-caution',
    text: 'text-caution',
    ring: 'ring-caution/25',
  },
  HIGH: {
    level: 'HIGH',
    label: 'HIGH RISK',
    color: '#FF9142',
    dot: 'bg-high',
    text: 'text-high',
    ring: 'ring-high/25',
  },
  CRITICAL: {
    level: 'CRITICAL',
    label: 'CRITICAL RISK',
    color: '#FF4D4F',
    dot: 'bg-critical',
    text: 'text-critical',
    ring: 'ring-critical/25',
  },
};

export const SEVERITY_ORDER = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];

// Looks up a severity by string, case-insensitive, with LOW as a safe fallback
// for unrecognized values (rather than crashing on bad backend data).
export function resolveSeverity(input) {
  const key = String(input ?? '').toUpperCase();
  return SEVERITY[key] ?? SEVERITY.LOW;
}

// Derives a canonical level from a 0-100 risk score, per the thresholds
// in PROJECT_CONTEXT.md. Only used when the backend hasn't sent an explicit
// `level` alongside the score.
export function levelFromScore(score) {
  if (score < 30) return 'LOW';
  if (score < 60) return 'MEDIUM';
  if (score < 80) return 'HIGH';
  return 'CRITICAL';
}
