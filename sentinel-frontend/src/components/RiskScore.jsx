import { TrendingDown, TrendingUp } from 'lucide-react';
import { resolveSeverity, levelFromScore } from '../constants/severity';

export default function RiskScore({ score = 0, level, trend = 0, lastScan }) {
  const clamped = Math.max(0, Math.min(100, score));
  const resolvedLevel = level ?? levelFromScore(clamped);
  const severity = resolveSeverity(resolvedLevel);

  // Semi-circular gauge geometry
  const radius = 72;
  const circumference = Math.PI * radius; // half circle
  const progress = (clamped / 100) * circumference;
  const trendDown = trend < 0; // negative trend = risk decreasing = good

  return (
    <div className="flex flex-col items-center rounded-lg border border-border bg-surface p-5 shadow-panel">
      <div className="flex w-full items-center justify-between">
        <p className="text-xs font-medium uppercase tracking-wide text-ink-muted">System Risk</p>
        <div
          className={[
            'flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-medium',
            trendDown ? 'bg-safe/10 text-safe' : 'bg-critical/10 text-critical',
          ].join(' ')}
        >
          {trendDown ? <TrendingDown size={12} /> : <TrendingUp size={12} />}
          {Math.abs(trend)} pts / 7d
        </div>
      </div>

      <div className="relative mt-2 h-[100px] w-[180px]">
        <svg viewBox="0 0 180 100" className="h-full w-full overflow-visible">
          {/* track */}
          <path
            d="M 18 92 A 72 72 0 0 1 162 92"
            fill="none"
            stroke="#1B222D"
            strokeWidth="12"
            strokeLinecap="round"
          />
          {/* tick marks — instrument-panel detail */}
          {Array.from({ length: 11 }).map((_, i) => {
            const angle = Math.PI - (i / 10) * Math.PI;
            const x1 = 90 + Math.cos(angle) * 80;
            const y1 = 92 - Math.sin(angle) * 80;
            const x2 = 90 + Math.cos(angle) * 86;
            const y2 = 92 - Math.sin(angle) * 86;
            return (
              <line
                key={i}
                x1={x1}
                y1={y1}
                x2={x2}
                y2={y2}
                stroke="#2A3546"
                strokeWidth="1.5"
              />
            );
          })}
          {/* value arc */}
          <path
            d="M 18 92 A 72 72 0 0 1 162 92"
            fill="none"
            stroke={severity.color}
            strokeWidth="12"
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
            style={{ filter: `drop-shadow(0 0 6px ${severity.color}66)` }}
          />
        </svg>
        <div className="absolute inset-x-0 bottom-0 flex flex-col items-center">
          <span className="font-mono text-3xl font-semibold tabular-nums text-ink">{clamped}</span>
          <span className="font-mono text-[11px] text-ink-muted">/ 100</span>
        </div>
      </div>

      <div className="mt-1 flex items-center gap-1.5">
        <span className={`h-1.5 w-1.5 rounded-full ${severity.dot}`} />
        <span className={`text-sm font-semibold tracking-wide ${severity.text}`}>{severity.label}</span>
      </div>

      {lastScan && <p className="mt-2 text-[11px] text-ink-muted">Last scan: {lastScan}</p>}
    </div>
  );
}
