import { useMemo, useState } from 'react';
import { Filter, Search } from 'lucide-react';
import EventTable from '../components/EventTable';
import ErrorState from '../components/ErrorState';
import LoadingSpinner from '../components/LoadingSpinner';
import { useApiResource } from '../hooks/useApiResource';
import { getEvents } from '../services/api';
import { recentThreats as mockEvents } from '../data/mockData';

const FILTERS = ['All', 'Critical', 'High', 'Medium', 'Low'];

export default function Events() {
  const { data: events, loading, error, retry } = useApiResource(getEvents, mockEvents);
  const [filter, setFilter] = useState('All');
  const [search, setSearch] = useState('');

  const filtered = useMemo(() => {
    const list = events ?? [];
    const query = search.trim().toLowerCase();
    return list.filter((e) => {
      const matchesFilter = filter === 'All' || e.severity.toLowerCase() === filter.toLowerCase();
      const matchesSearch =
        !query || e.title.toLowerCase().includes(query) || e.process.toLowerCase().includes(query);
      return matchesFilter && matchesSearch;
    });
  }, [events, filter, search]);

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
            placeholder="Search events…"
            className="w-48 bg-transparent text-xs text-ink placeholder:text-ink-muted focus:outline-none"
          />
        </div>
      </div>

      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        {loading ? <LoadingSpinner label="Loading events…" /> : <EventTable events={filtered} />}
      </div>
    </div>
  );
}