const RISK_META = {
  critical: { icon: '🔴', label: 'CRITICAL', text: 'text-critical' },
  high: { icon: '🟠', label: 'HIGH', text: 'text-high' },
  medium: { icon: '🟡', label: 'MEDIUM', text: 'text-caution' },
  low: { icon: '🟢', label: 'LOW', text: 'text-safe' },
};

// Match prototype accents for high-severity PowerShell events.
const EVENT_RISK_ICON = {
  'PowerShell Activity': '🔴',
};

export default function EventTable({ events = [] }) {
  if (events.length === 0) {
    return (
      <p className="py-10 text-center text-sm text-ink-muted">
        No events match your filter or search.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr className="border-b border-border text-left text-[11px] uppercase tracking-wide text-ink-muted">
            <th className="pb-3 pr-4 font-medium">Time</th>
            <th className="pb-3 pr-4 font-medium">Event</th>
            <th className="pb-3 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody>
          {events.map((item) => {
            const meta = RISK_META[item.risk] ?? RISK_META.low;
            const icon = EVENT_RISK_ICON[item.event] ?? meta.icon;

            return (
              <tr
                key={item.id}
                className="border-b border-border-muted transition-colors last:border-b-0 hover:bg-surface-hover"
              >
                <td className="py-3 pr-4 font-mono text-xs text-ink-secondary">{item.time}</td>
                <td className="py-3 pr-4 font-medium text-ink">{item.event}</td>
                <td className={`py-3 font-semibold ${meta.text}`}>
                  <span className="inline-flex items-center gap-2">
                    <span aria-hidden="true">{icon}</span>
                    <span>{meta.label}</span>
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
