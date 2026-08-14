import { Terminal, Clock, ArrowRight } from 'lucide-react';
import { resolveSeverity } from '../constants/severity';

/**
 * Reusable threat card. Renders any threat object shaped like:
 * {
 *   id: 1,
 *   severity: "high",              // low | medium | high | critical
 *   title: "Suspicious PowerShell Activity",
 *   description: "Unusual PowerShell behavior detected.",
 *   process: "powershell.exe",
 *   timestamp: "10:42 AM"
 * }
 *
 * onViewAnalysis(threat) is called when the button is clicked — wire this
 * up to the AI Explanation panel once that's built (build order item 9).
 */
export default function ThreatCard({ threat, reviewed = false, onViewAnalysis = () => {} }) {
  const severity = resolveSeverity(threat.severity);

  return (
    <div className={`rounded-lg border border-border bg-surface p-4 ring-1 ring-inset ${severity.ring} transition-colors hover:border-border-muted`}>
      <div className="flex items-center gap-2">
        <span className={`h-2 w-2 rounded-full ${severity.dot}`} />
        <span className={`text-xs font-semibold tracking-wide ${severity.text}`}>{severity.label}</span>
        {reviewed && (
          <span className="ml-auto text-[11px] font-medium text-safe">Reviewed</span>
        )}
      </div>

      <h3 className="mt-2.5 text-sm font-semibold text-ink">{threat.title}</h3>
      <p className="mt-1 text-sm leading-relaxed text-ink-secondary">{threat.description}</p>

      <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1.5 border-t border-border-muted pt-3">
        <div className="flex items-center gap-1.5 text-xs text-ink-muted">
          <Terminal size={13} />
          <span>
            Process: <span className="font-mono text-ink-secondary">{threat.process}</span>
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-xs text-ink-muted">
          <Clock size={13} />
          <span>
            Time: <span className="font-mono text-ink-secondary">{threat.timestamp}</span>
          </span>
        </div>
      </div>

      <button
        type="button"
        onClick={() => onViewAnalysis(threat)}
        className="mt-3 flex w-full items-center justify-center gap-1.5 rounded-md border border-accent/30 bg-accent/[0.06] py-2 text-xs font-medium text-accent transition-colors hover:bg-accent/[0.12]"
      >
        View Analysis
        <ArrowRight size={13} />
      </button>
    </div>
  );
}