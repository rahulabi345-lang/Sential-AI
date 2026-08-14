import { useState } from 'react';
import { Search, ChevronDown } from 'lucide-react';
import { securityEvents, getThreatAnalysis } from '../data/mockData';
import { resolveSeverity, SEVERITY_ORDER } from '../constants/severity';
import AIExplanation from '../components/AIExplanation';

const FILTERS = ['ALL', ...SEVERITY_ORDER];

export default function Events() {
  const [filter, setFilter] = useState('ALL');
  const [filterOpen, setFilterOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [reviewedIds, setReviewedIds] = useState([]);

  const filtered = securityEvents.filter((e) => {
    const matchesFilter = filter === 'ALL' || e.severity.toUpperCase() === filter;
    const matchesSearch = `${e.title} ${e.device}`.toLowerCase().includes(search.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-5">
      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <div className="flex items-center gap-3">
          <div className="relative">
            <button
              onClick={() => setFilterOpen((o) => !o)}
              className="flex items-center gap-2 rounded-md border border-border bg-surface px-3 py-2 text-sm font-medium text-ink min-w-[130px] justify-between"
            >
              <span className="capitalize">{filter === 'ALL' ? 'All' : filter}</span>
              <ChevronDown size={14} className="text-ink-muted" />
            </button>
            {filterOpen && (
              <div className="absolute top-full mt-1 left-0 z-10 min-w-[150px] rounded-md border border-border bg-surface-raised p-1 shadow-panel">
                {FILTERS.map((f) => (
                  <div
                    key={f}
                    onClick={() => { setFilter(f); setFilterOpen(false); }}
                    className="cursor-pointer rounded-sm px-3 py-2 text-sm text-ink-secondary hover:bg-surface-hover hover:text-ink"
                  >
                    {f === 'ALL' ? 'All' : resolveSeverity(f).label.replace(' RISK', '')}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="relative flex-1 max-w-xs">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-muted" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search events or devices…"
              className="w-full rounded-md border border-border bg-surface py-2 pl-8 pr-3 text-sm text-ink placeholder:text-ink-muted focus:border-accent focus:outline-none"
            />
          </div>

          <span className="text-xs text-ink-muted whitespace-nowrap">
            {filtered.length} of {securityEvents.length} events
          </span>
        </div>

        <div className="mt-4 rounded-lg border border-border overflow-hidden">
          <div className="grid grid-cols-[80px_1fr_140px_110px] border-b border-border px-5 py-3 text-xs font-semibold uppercase tracking-wide text-ink-muted">
            <span>Time</span><span>Event</span><span>Device</span><span className="text-right">Risk</span>
          </div>
          {filtered.map((e) => {
            const severity = resolveSeverity(e.severity);
            const reviewed = reviewedIds.includes(e.id);
            return (
              <div
                key={e.id}
                onClick={() => setSelectedEvent(e)}
                className="grid grid-cols-[80px_1fr_140px_110px] items-center border-b border-border px-5 py-3 last:border-0 cursor-pointer hover:bg-surface-hover"
              >
                <span className="font-mono text-xs text-ink-muted">{e.timestamp}</span>
                <span className="flex items-center gap-2 text-sm font-medium text-ink">
                  {e.title}
                  {reviewed && <span className="text-[10px] font-semibold text-safe">· Reviewed</span>}
                </span>
                <span className="truncate font-mono text-xs text-ink-muted">{e.device}</span>
                <span className="flex justify-end items-center gap-1.5">
                  <span className={`h-1.5 w-1.5 rounded-full ${severity.dot}`} />
                  <span className={`text-xs font-semibold tracking-wide ${severity.text}`}>{severity.level}</span>
                </span>
              </div>
            );
          })}
          {filtered.length === 0 && (
            <div className="py-16 text-center text-sm text-ink-muted">No events match your filter.</div>
          )}
        </div>
      </div>

      {selectedEvent && (
        <AIExplanation
          threat={selectedEvent}
          analysis={getThreatAnalysis(selectedEvent)}
          reviewed={reviewedIds.includes(selectedEvent.id)}
          onClose={() => setSelectedEvent(null)}
          onMarkReviewed={() =>
            setReviewedIds((ids) => [...ids, selectedEvent.id])
          }
        />
      )}
    </div>
  );
}