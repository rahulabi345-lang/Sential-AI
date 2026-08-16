import { useMemo, useState } from 'react';
import { Filter, Search } from 'lucide-react';
import ThreatCard from '../components/ThreatCard';
import ThreatCardSkeleton from '../components/skeletons/ThreatCardSkeleton';
import ErrorState from '../components/ErrorState';
import AIExplanation from '../components/AIExplanation';
import LoadingSpinner from '../components/LoadingSpinner';
import { useApiResource } from '../hooks/useApiResource';
import { useThreatAnalysisPanel } from '../hooks/useThreatAnalysisPanel';
import { getThreats } from '../services/api';
import { recentThreats as mockThreats } from '../data/mockData';

const FILTERS = ['All', 'Critical', 'High', 'Medium', 'Low'];

export default function Threats() {
  const { data: threats, loading, error, retry } = useApiResource(getThreats, mockThreats);
  const [filter, setFilter] = useState('All');
  const [search, setSearch] = useState('');

  const {
    selectedThreat,
    analysis,
    analysisLoading,
    reviewedIds,
    openThreat,
    closeThreat,
    handleMarkReviewed,
  } = useThreatAnalysisPanel(threats);

  const filtered = useMemo(() => {
    const list = threats ?? [];
    const query = search.trim().toLowerCase();
    return list.filter((t) => {
      const matchesFilter = filter === 'All' || t.severity.toLowerCase() === filter.toLowerCase();
      const matchesSearch =
        !query ||
        t.title.toLowerCase().includes(query) ||
        t.process.toLowerCase().includes(query) ||
        t.description.toLowerCase().includes(query);
      return matchesFilter && matchesSearch;
    });
  }, [threats, filter, search]);

  if (error) {
    return <ErrorState onRetry={retry} />;
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-3 rounded-lg border border-border bg-surface p-4">
        <div className="flex items-center gap-2 text-ink-muted">
          <Filter size={15} />
          <span className="text-xs font-medium">Filter:</span>
        </div>
        <div className="flex flex-wrap gap-1.5">
          {FILTERS.map((f) => (
            <button
              key={f}
              type="button"
              onClick={() => setFilter(f)}
              className={[
                'rounded-md px-3 py-1.5 text-xs font-medium transition-colors',
                filter === f
                  ? 'bg-accent/15 text-accent ring-1 ring-inset ring-accent/30'
                  : 'text-ink-secondary hover:bg-surface-hover',
              ].join(' ')}
            >
              {f}
            </button>
          ))}
        </div>
        <div className="ml-auto flex items-center gap-2 rounded-md border border-border bg-canvas px-3 py-1.5 text-ink-muted">
          <Search size={14} />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search threats…"
            className="w-48 bg-transparent text-xs text-ink placeholder:text-ink-muted focus:outline-none"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
        {loading ? (
          <>
            <ThreatCardSkeleton />
            <ThreatCardSkeleton />
            <ThreatCardSkeleton />
            <ThreatCardSkeleton />
            <ThreatCardSkeleton />
            <ThreatCardSkeleton />
          </>
        ) : filtered.length === 0 ? (
          <p className="col-span-full py-10 text-center text-sm text-ink-muted">
            No threats match your filter or search.
          </p>
        ) : (
          filtered.map((threat) => (
            <ThreatCard
              key={threat.id}
              threat={threat}
              reviewed={reviewedIds.includes(threat.id)}
              onViewAnalysis={openThreat}
            />
          ))
        )}
      </div>

      {selectedThreat && analysisLoading && !analysis && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
          <div className="rounded-lg border border-border bg-surface p-6 shadow-panel">
            <LoadingSpinner label="Loading AI analysis…" />
          </div>
        </div>
      )}

      {selectedThreat && analysis && (
        <AIExplanation
          threat={selectedThreat}
          analysis={analysis}
          reviewed={reviewedIds.includes(selectedThreat.id)}
          onClose={closeThreat}
          onMarkReviewed={handleMarkReviewed}
        />
      )}
    </div>
  );
}