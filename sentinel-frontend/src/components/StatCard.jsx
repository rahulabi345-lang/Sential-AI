// Small reusable metric tile — used for the stat row on the dashboard
// (threat count, event count, critical alerts, overall status).
// Not part of the original file list but split out because these four
// tiles share identical layout logic; keeping it inline in Dashboard.jsx
// would duplicate the same markup four times.
export default function StatCard({ icon: Icon, label, value, tone = 'default', hint }) {
  const toneStyles = {
    default: 'text-ink',
    safe: 'text-safe',
    critical: 'text-critical',
    high: 'text-high',
    accent: 'text-accent',
  };

  return (
    <div className="rounded-lg border border-border bg-surface p-4 shadow-panel">
      <div className="flex items-center justify-between">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-muted">{label}</p>
        {Icon && <Icon size={15} className="text-ink-muted" />}
      </div>
      <p className={`mt-2 font-mono text-2xl font-semibold tabular-nums ${toneStyles[tone]}`}>{value}</p>
      {hint && <p className="mt-1 text-[11px] text-ink-muted">{hint}</p>}
    </div>
  );
}
