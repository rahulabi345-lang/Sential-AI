const STATUS_META = {
  active: { label: 'Active', dot: 'bg-safe', text: 'text-safe' },
  warning: { label: 'Attention', dot: 'bg-caution', text: 'text-caution' },
  inactive: { label: 'Inactive', dot: 'bg-critical', text: 'text-critical' },
};

export default function SecurityStatus({ systems = [] }) {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <p className="text-sm font-semibold text-ink">System Status</p>
      <p className="text-xs text-ink-muted">Protection components monitored in real time</p>

      <div className="mt-4 space-y-1">
        {systems.map((system) => {
          const meta = STATUS_META[system.status] ?? STATUS_META.warning;
          return (
            <div
              key={system.id}
              className="flex items-center gap-3 rounded-md px-2 py-2.5 transition-colors hover:bg-surface-hover"
            >
              <span className={`h-2 w-2 shrink-0 rounded-full ${meta.dot}`} />
              <div className="min-w-0 flex-1">
                <p className="text-sm text-ink">{system.name}</p>
                <p className="truncate text-[11px] text-ink-muted">{system.detail}</p>
              </div>
              <span className={`shrink-0 text-[11px] font-medium ${meta.text}`}>{meta.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
