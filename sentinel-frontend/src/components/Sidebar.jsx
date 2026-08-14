import {
  LayoutDashboard,
  ShieldAlert,
  ListTree,
  FileBarChart2,
  Settings,
  ShieldCheck,
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'threats', label: 'Threats', icon: ShieldAlert },
  { id: 'events', label: 'Security Events', icon: ListTree },
  { id: 'reports', label: 'Reports', icon: FileBarChart2 },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ activePage = 'dashboard', onNavigate = () => {} }) {
  return (
    <aside className="flex h-screen w-60 shrink-0 flex-col border-r border-border bg-surface">
      <div className="flex items-center gap-2.5 px-5 py-5">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-accent/10 text-accent ring-1 ring-accent/30">
          <ShieldCheck size={18} strokeWidth={2.25} />
        </div>
        <div className="leading-tight">
          <p className="font-display text-[15px] font-semibold tracking-tight text-ink">Sentinel AI</p>
          <p className="text-[11px] text-ink-muted">Endpoint Security</p>
        </div>
      </div>

      <nav className="mt-2 flex-1 space-y-0.5 px-3">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => {
          const isActive = activePage === id;
          return (
            <button
              key={id}
              type="button"
              onClick={() => onNavigate(id)}
              aria-current={isActive ? 'page' : undefined}
              className={[
                'group flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
                isActive
                  ? 'bg-accent/10 text-ink ring-1 ring-inset ring-accent/25'
                  : 'text-ink-secondary hover:bg-surface-hover hover:text-ink',
              ].join(' ')}
            >
              <Icon
                size={17}
                strokeWidth={2}
                className={isActive ? 'text-accent' : 'text-ink-muted group-hover:text-ink-secondary'}
              />
              <span className="font-medium">{label}</span>
              {isActive && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-accent shadow-glow" />}
            </button>
          );
        })}
      </nav>

      <div className="mx-3 mb-4 rounded-md border border-border-muted bg-canvas/60 px-3 py-2.5">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-safe opacity-40" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-safe" />
          </span>
          <p className="text-xs font-medium text-ink-secondary">Monitoring active</p>
        </div>
        <p className="mt-1 font-mono text-[11px] text-ink-muted">Agent v2.4.1 · Online</p>
      </div>
    </aside>
  );
}
