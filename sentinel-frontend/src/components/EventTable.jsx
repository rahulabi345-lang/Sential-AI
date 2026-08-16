import { resolveSeverity } from '../constants/severity';

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
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-border text-xs uppercase tracking-wide text-ink-muted">
            <th className="py-2 pr-4 font-medium">Time</th>
            <th className="py-2 pr-4 font-medium">Event</th>
            <th className="py-2 pr-4 font-medium">Process</th>
            <th className="py-2 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => {
            const severity = resolveSeverity(event.severity);
            return (
              <tr
                key={event.id}
                className="border-b border-border-muted last:border-0 hover:bg-surface-hover"
              >
                <td className="py-2.5 pr-4 font-mono text-xs text-ink-muted">{event.timestamp}</td>
                <td className="py-2.5 pr-4 text-ink">{event.title}</td>
                <td className="py-2.5 pr-4 font-mono text-xs text-ink-secondary">{event.process}</td>
                <td className="py-2.5">
                  <span className={`inline-flex items-center gap-1.5 text-xs font-semibold ${severity.text}`}>
                    <span className={`h-1.5 w-1.5 rounded-full ${severity.dot}`} />
                    {severity.level}
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