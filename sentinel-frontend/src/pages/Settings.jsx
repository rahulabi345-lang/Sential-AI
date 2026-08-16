import { useState } from 'react';
import { Bell, RefreshCw } from 'lucide-react';

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={[
        'relative h-6 w-11 shrink-0 rounded-full transition-colors',
        checked ? 'bg-accent' : 'bg-surface-hover',
      ].join(' ')}
    >
      <span
        className={[
          'absolute top-0.5 h-5 w-5 rounded-full bg-canvas transition-transform',
          checked ? 'translate-x-[22px]' : 'translate-x-0.5',
        ].join(' ')}
      />
    </button>
  );
}

function SettingRow({ icon: Icon, title, description, control }) {
  return (
    <div className="flex items-center gap-4 border-b border-border-muted py-4 last:border-0">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-surface-raised text-ink-muted">
        <Icon size={16} />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-ink">{title}</p>
        <p className="text-xs text-ink-muted">{description}</p>
      </div>
      {control}
    </div>
  );
}

export default function Settings() {
  const [notifications, setNotifications] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [scanFrequency, setScanFrequency] = useState('15');

  return (
    <div className="max-w-2xl space-y-5">
      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <p className="text-sm font-semibold text-ink">Notifications</p>
        <p className="text-xs text-ink-muted">Control how Sentinel AI alerts you</p>

        <div className="mt-2">
          <SettingRow
            icon={Bell}
            title="Threat notifications"
            description="Get notified when a new threat is detected"
            control={<Toggle checked={notifications} onChange={setNotifications} />}
          />
          <SettingRow
            icon={RefreshCw}
            title="Auto-refresh dashboard"
            description="Keep security data up to date automatically"
            control={<Toggle checked={autoRefresh} onChange={setAutoRefresh} />}
          />
        </div>
      </div>

      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <p className="text-sm font-semibold text-ink">Scanning</p>
        <p className="text-xs text-ink-muted">Configure how often the system scans for threats</p>

        <div className="mt-4 flex items-center justify-between">
          <div>
            <p className="text-sm text-ink">Scan frequency</p>
            <p className="text-xs text-ink-muted">How often Sentinel AI checks for new activity</p>
          </div>
          <select
            value={scanFrequency}
            onChange={(e) => setScanFrequency(e.target.value)}
            className="rounded-md border border-border bg-canvas px-3 py-1.5 text-xs text-ink focus:outline-none"
          >
            <option value="5">Every 5 minutes</option>
            <option value="15">Every 15 minutes</option>
            <option value="30">Every 30 minutes</option>
            <option value="60">Every hour</option>
          </select>
        </div>
      </div>

      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <p className="text-sm font-semibold text-ink">About</p>
        <div className="mt-3 space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-ink-muted">Agent version</span>
            <span className="font-mono text-ink">v2.4.1</span>
          </div>
          <div className="flex justify-between">
            <span className="text-ink-muted">Status</span>
            <span className="flex items-center gap-1.5 text-safe">
              <span className="h-1.5 w-1.5 rounded-full bg-safe" />
              Online
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}