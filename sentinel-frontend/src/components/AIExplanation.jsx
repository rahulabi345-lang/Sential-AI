
/**
 * Slide-over panel shown when a threat card's "View Analysis" is clicked.
 * threat: the base threat object (same shape as ThreatCard's prop)
 * analysis: { summary, whySuspicious[], recommendation } — see
 *           data/mockData.js getThreatAnalysis() for the mock version.
 */import { Bot, X, CheckCircle2 } from 'lucide-react';
import { resolveSeverity } from '../constants/severity';

export default function AIExplanation({ threat, analysis, reviewed = false, onClose, onMarkReviewed }) {
  if (!threat || !analysis) return null;
  const severity = resolveSeverity(threat.severity);

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />

      <div className="relative flex h-full w-full max-w-md flex-col border-l border-border bg-surface shadow-panel">
        <div className="flex items-center justify-between border-b border-border px-5 py-4">
          <div className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-md bg-accent/10 text-accent ring-1 ring-accent/30">
              <Bot size={16} />
            </div>
            <p className="font-display text-sm font-semibold text-ink">Sentinel AI Analysis</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="flex h-8 w-8 items-center justify-center rounded-md text-ink-muted transition-colors hover:bg-surface-hover hover:text-ink"
          >
            <X size={16} />
          </button>
        </div>

        <div className="flex-1 space-y-5 overflow-y-auto px-5 py-5">
          <div>
            <p className="text-xs uppercase tracking-wide text-ink-muted">Threat</p>
            <p className="mt-1 text-sm font-semibold text-ink">{threat.title}</p>
            <div className="mt-2 flex items-center gap-1.5">
              <span className={`h-1.5 w-1.5 rounded-full ${severity.dot}`} />
              <span className={`text-xs font-semibold tracking-wide ${severity.text}`}>{severity.label}</span>
            </div>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ink-muted">What happened?</p>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-secondary">{analysis.summary}</p>
          </div>

          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-ink-muted">Why is this suspicious?</p>
            <ul className="mt-1.5 space-y-1.5">
              {analysis.whySuspicious.map((point) => (
                <li key={point} className="flex items-start gap-2 text-sm text-ink-secondary">
                  <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-ink-muted" />
                  {point}
                </li>
              ))}
            </ul>
          </div>

          <div className="rounded-md border border-accent/25 bg-accent/[0.05] p-3">
            <p className="text-xs font-semibold uppercase tracking-wide text-accent">Recommended Action</p>
            <p className="mt-1.5 text-sm leading-relaxed text-ink-secondary">{analysis.recommendation}</p>
          </div>
        </div>

        <div className="border-t border-border px-5 py-4">
          <button
            type="button"
            onClick={onMarkReviewed}
            disabled={reviewed}
            className={[
              'flex w-full items-center justify-center gap-2 rounded-md py-2.5 text-sm font-medium transition-colors',
              reviewed
                ? 'cursor-default border border-safe/30 bg-safe/10 text-safe'
                : 'bg-accent text-canvas hover:bg-accent/90',
            ].join(' ')}
          >
            <CheckCircle2 size={15} />
            {reviewed ? 'Reviewed' : 'Mark as Reviewed'}
          </button>
        </div>
      </div>
    </div>
  );
}