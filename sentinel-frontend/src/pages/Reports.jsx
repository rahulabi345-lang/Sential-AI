import { useMemo } from 'react';
import { FileText, Download } from 'lucide-react';
import ErrorState from '../components/ErrorState';
import LoadingSpinner from '../components/LoadingSpinner';
import { useApiResource } from '../hooks/useApiResource';
import { getThreats } from '../services/api';
import { recentThreats as mockThreats } from '../data/mockData';
import { SEVERITY_ORDER, resolveSeverity } from '../constants/severity';

export default function Reports() {
  const { data: threats, loading, error, retry } = useApiResource(getThreats, mockThreats);

  const breakdown = useMemo(() => {
    const list = threats ?? [];
    const counts = { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 };
    list.forEach((t) => {
      const level = resolveSeverity(t.severity).level;
      counts[level] = (counts[level] ?? 0) + 1;
    });
    return counts;
  }, [threats]);

  const total = threats?.length ?? 0;

  if (error) {
    return <ErrorState onRetry={retry} />;
  }

  if (loading) {
    return <LoadingSpinner label="Generating report…" />;
  }

  const generatedAt = new Date().toLocaleString('en-US', {
    dateStyle: 'medium',
    timeStyle: 'short',
  });

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between rounded-lg border border-border bg-surface p-5 shadow-panel">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-md bg-accent/10 text-accent">
            <FileText size={18} />
          </div>
          <div>
            <p className="text-sm font-semibold text-ink">Security Summary Report</p>
            <p className="text-xs text-ink-muted">Generated {generatedAt}</p>
          </div>
        </div>
        <button
          type="button"
          className="flex items-center gap-1.5 rounded-md border border-border bg-canvas px-3 py-1.5 text-xs font-medium text-ink-secondary hover:bg-surface-hover"
        >
          <Download size={13} />
          Export
        </button>
      </div>

      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <p className="text-sm font-semibold text-ink">Threat Breakdown</p>
        <p className="text-xs text-ink-muted">{total} total threats recorded this period</p>

        <div className="mt-4 space-y-3">
          {SEVERITY_ORDER.slice().reverse().map((level) => {
            const severity = resolveSeverity(level);
            const count = breakdown[level] ?? 0;
            const pct = total > 0 ? Math.round((count / total) * 100) : 0;
            return (
              <div key={level}>
                <div className="flex items-center justify-between text-xs">
                  <span className={`flex items-center gap-1.5 font-medium ${severity.text}`}>
                    <span className={`h-1.5 w-1.5 rounded-full ${severity.dot}`} />
                    {level}
                  </span>
                  <span className="font-mono text-ink-muted">
                    {count} ({pct}%)
                  </span>
                </div>
                <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-surface-hover">
                  <div className={`h-full rounded-full ${severity.dot}`} style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <p className="text-sm font-semibold text-ink">Summary</p>
        <p className="mt-2 text-sm leading-relaxed text-ink-secondary">
          This report reflects {total} tracked threat{total === 1 ? '' : 's'} across all severity
          levels.{' '}
          {breakdown.CRITICAL > 0
            ? `${breakdown.CRITICAL} critical threat${breakdown.CRITICAL === 1 ? '' : 's'} ${breakdown.CRITICAL === 1 ? 'requires' : 'require'} immediate attention.`
            : 'No critical threats are currently outstanding.'}
        </p>
      </div>
    </div>
  );
}