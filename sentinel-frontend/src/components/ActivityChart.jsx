import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-md border border-border bg-surface-raised px-3 py-2 shadow-panel">
      <p className="mb-1 text-[11px] font-medium text-ink-secondary">{label}</p>
      {payload.map((entry) => (
        <div key={entry.dataKey} className="flex items-center gap-2 text-xs">
          <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-ink-muted capitalize">{entry.dataKey}</span>
          <span className="ml-auto font-mono font-medium text-ink">{entry.value}</span>
        </div>
      ))}
    </div>
  );
}

export default function ActivityChart({ data = [] }) {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-ink">Security Activity</p>
          <p className="text-xs text-ink-muted">Threats detected vs. blocked, last 7 days</p>
        </div>
        <div className="flex items-center gap-3 text-[11px] text-ink-muted">
          <div className="flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-info" />
            Detected
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            Blocked
          </div>
        </div>
      </div>

      <div className="mt-4 h-56">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="detectedFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#4EA1FF" stopOpacity={0.25} />
                <stop offset="100%" stopColor="#4EA1FF" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="blockedFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#2FDFC7" stopOpacity={0.3} />
                <stop offset="100%" stopColor="#2FDFC7" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#171E29" vertical={false} />
            <XAxis
              dataKey="day"
              stroke="#56626F"
              tick={{ fill: '#8291A3', fontSize: 11 }}
              axisLine={{ stroke: '#212A38' }}
              tickLine={false}
            />
            <YAxis
              stroke="#56626F"
              tick={{ fill: '#8291A3', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              width={28}
            />
            <Tooltip content={<ChartTooltip />} cursor={{ stroke: '#212A38' }} />
            <Area
              type="monotone"
              dataKey="detected"
              stroke="#4EA1FF"
              strokeWidth={2}
              fill="url(#detectedFill)"
            />
            <Area
              type="monotone"
              dataKey="blocked"
              stroke="#2FDFC7"
              strokeWidth={2}
              fill="url(#blockedFill)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
