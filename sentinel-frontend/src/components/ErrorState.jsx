import { ShieldAlert } from 'lucide-react';

export default function ErrorState({
  title = 'Unable to connect to Sentinel AI engine',
  message = 'The security service is currently unavailable.',
  onRetry,
}) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-critical/25 bg-critical/[0.05] px-6 py-14 text-center">
      <div className="flex h-11 w-11 items-center justify-center rounded-full bg-critical/10 text-critical">
        <ShieldAlert size={20} />
      </div>
      <p className="mt-4 text-sm font-semibold text-ink">{title}</p>
      <p className="mt-1 max-w-sm text-xs text-ink-muted">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-5 rounded-md bg-accent px-4 py-2 text-xs font-semibold text-canvas hover:bg-accent/90"
        >
          Retry Connection
        </button>
      )}
    </div>
  );
}