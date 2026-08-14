import { useDemoMode } from '../context/DemoModeContext';

export default function ModeToggle() {
  const { mode, toggleMode } = useDemoMode();
  const isLive = mode === 'live';

  return (
    <button
      type="button"
      onClick={toggleMode}
      title="Toggle between live backend data and demo data"
      className="flex items-center gap-2 rounded-full border border-border bg-surface px-3 py-1.5 text-xs font-semibold"
    >
      <span className={`h-1.5 w-1.5 rounded-full ${isLive ? 'bg-safe' : 'bg-accent'}`} />
      <span className={isLive ? 'text-safe' : 'text-accent'}>{isLive ? 'LIVE' : 'DEMO'}</span>
    </button>
  );
}