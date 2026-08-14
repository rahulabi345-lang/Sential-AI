import { Construction } from 'lucide-react';

// Placeholder — built in a later phase (see PROJECT_CONTEXT.md build order).
export default function Settings() {
  return (
    <div className="flex h-[60vh] flex-col items-center justify-center rounded-lg border border-dashed border-border text-center">
      <Construction size={22} className="text-ink-muted" />
      <p className="mt-3 text-sm font-medium text-ink">Settings is coming up next</p>
      <p className="mt-1 max-w-xs text-xs text-ink-muted">
        This section isn't built yet — the dashboard was the first milestone.
      </p>
    </div>
  );
}
