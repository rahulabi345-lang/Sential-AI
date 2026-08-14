import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

function ChartTooltip({ active, payload }) {
  if (!active || !payload?.length) return null;
  const entry = payload[0];
  return (
    <div className="rounded-md border border-border bg-surface-raised px-3 py-2 shadow-panel">
      <div className="flex items-center gap-2 text-xs">
        <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: entry.payload.color }} />
        <span className="text-ink-muted">{entry.name}</span>
        <span className="ml-auto font-mono font-medium text-ink">{entry.value}%</span>
      </div>
    </div>
  );
}

export default function RiskDistributionChart({ data = [] }) {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <div>
        <p className="text-sm font-semibold text-ink">Threat Distribution</p>
        <p className="text-xs text-ink-muted">Detections by risk level</p>
      </div>

      <div className="mt-4 flex items-center gap-5">
        <div className="h-40 w-40 shrink-0">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey="value"
                nameKey="name"
                innerRadius={44}
                outerRadius={70}
                paddingAngle={3}
                stroke="none"
              >
                {data.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip content={<ChartTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="flex-1 space-y-2.5">
          {data.map((entry) => (
            <div key={entry.name} className="flex items-center gap-2 text-xs">
              <span className="h-1.5 w-1.5 rounded-full" style={{ backgroundColor: entry.color }} />
              <span className="text-ink-secondary">{entry.name}</span>
              <span className="ml-auto font-mono font-medium text-ink">{entry.value}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}