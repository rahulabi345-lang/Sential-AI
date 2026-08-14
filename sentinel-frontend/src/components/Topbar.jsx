import { Bell, Search, ChevronDown } from 'lucide-react';
import { notifications } from '../data/mockData';

export default function Topbar({ title = 'Dashboard', subtitle }) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-border bg-surface/60 px-6 backdrop-blur">
      <div>
        <h1 className="font-display text-[17px] font-semibold tracking-tight text-ink">{title}</h1>
        {subtitle && <p className="text-xs text-ink-muted">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-md border border-border bg-canvas px-3 py-1.5 text-ink-muted sm:flex">
          <Search size={14} />
          <input
            type="text"
            placeholder="Search threats, events, IPs…"
            className="w-56 bg-transparent text-xs text-ink placeholder:text-ink-muted focus:outline-none"
          />
          <kbd className="rounded border border-border px-1.5 py-0.5 font-mono text-[10px] text-ink-muted">⌘K</kbd>
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-9 w-9 items-center justify-center rounded-md border border-border bg-canvas text-ink-secondary transition-colors hover:text-ink"
        >
          <Bell size={16} />
          {notifications.unreadCount > 0 && (
            <span className="absolute -right-1 -top-1 flex h-4 min-w-4 items-center justify-center rounded-full bg-critical px-1 font-mono text-[10px] font-semibold text-white">
              {notifications.unreadCount}
            </span>
          )}
        </button>

        <button
          type="button"
          className="flex items-center gap-2 rounded-md border border-border bg-canvas py-1.5 pl-1.5 pr-2.5 hover:bg-surface-hover"
        >
          <div className="flex h-6 w-6 items-center justify-center rounded-sm bg-accent/15 font-mono text-[11px] font-semibold text-accent">
            A
          </div>
          <span className="text-xs font-medium text-ink-secondary">Admin</span>
          <ChevronDown size={13} className="text-ink-muted" />
        </button>
      </div>
    </header>
  );
}
