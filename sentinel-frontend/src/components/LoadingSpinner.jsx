import { LoaderCircle } from 'lucide-react';

// Reusable loading state — will be used once real API calls (services/api.js)
// replace the mock data imports.
export default function LoadingSpinner({ label = 'Loading…', size = 18 }) {
  return (
    <div className="flex items-center justify-center gap-2 py-8 text-ink-muted">
      <LoaderCircle size={size} className="animate-spin" />
      <span className="text-xs">{label}</span>
    </div>
  );
}
