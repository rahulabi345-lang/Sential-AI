import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-md border border-border bg-surface-raised px-3 py-2 shadow-panel">
      <p className="mb-1 text-[11px] font-medium text-ink-secondary">{label}</p>
      <div className="flex items-center gap-2 text-xs">
        <span className="h-1.5 w-1.5 rounded-full bg-info" />
        <span className="text-ink-muted">Events</span>
        <span className="ml-auto font-mono font-medium text-ink">{payload[0].value}</span>
      </div>
    </div>
  );
}

export default function CategoryActivityChart({ data = [] }) {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <div>
        <p className="text-sm font-semibold text-ink">Activity by Category</p>
        <p className="text-xs text-ink-muted">Where detections are happening</p>
      </div>

      <div className="mt-4 h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 4, right: 16, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#171E29" horizontal={false} />
            <XAxis
              type="number"
              stroke="#56626F"
              tick={{ fill: '#8291A3', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              type="category"
              dataKey="category"
              stroke="#56626F"
              tick={{ fill: '#8291A3', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              width={92}
            />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: '#171E29' }} />
            <Bar dataKey="count" fill="#4EA1FF" radius={[0, 4, 4, 0]} barSize={14} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}