import { useEffect, useState } from 'react';
import { ShieldCheck, Bug, ListTree, Siren } from 'lucide-react';
import RiskScore from '../components/RiskScore';
import StatCard from '../components/StatCard';
import ActivityChart from '../components/ActivityChart';
import RiskDistributionChart from '../components/RiskDistributionChart';
import CategoryActivityChart from '../components/CategoryActivityChart';
import ThreatCard from '../components/ThreatCard';
import SecurityStatus from '../components/SecurityStatus';
import AIExplanation from '../components/AIExplanation';
import ErrorState from '../components/ErrorState';
import ModeToggle from '../components/ModeToggle';
import LoadingSpinner from '../components/LoadingSpinner';
import StatCardSkeleton from '../components/skeletons/StatCardSkeleton';
import ThreatCardSkeleton from '../components/skeletons/ThreatCardSkeleton';
import { SkeletonBar } from '../components/skeletons/Skeleton';
import { useApiResource } from '../hooks/useApiResource';
import { useDemoMode } from '../context/DemoModeContext';
import { getDashboard, getThreats, getThreatAnalysis as fetchAnalysisFromApi } from '../services/api';
import {
  securityOverview as mockOverview,
  recentThreats as mockThreats,
  activityData,
  systemStatus,
  riskDistribution,
  categoryActivity,
  getThreatAnalysis as getMockAnalysis,
} from '../data/mockData';

export default function Dashboard() {
  const { isDemo } = useDemoMode();

  const {
    data: overview,
    loading: overviewLoading,
    error: overviewError,
    retry: retryOverview,
  } = useApiResource(getDashboard, mockOverview);

  const {
    data: threats,
    loading: threatsLoading,
    error: threatsError,
    retry: retryThreats,
  } = useApiResource(getThreats, mockThreats);

  const [selectedThreatId, setSelectedThreatId] = useState(null);
  const [reviewedIds, setReviewedIds] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const selectedThreat = (threats ?? []).find((t) => t.id === selectedThreatId) ?? null;

  // Fetch (or look up) the AI analysis whenever the selected threat changes.
  useEffect(() => {
    if (!selectedThreat) {
      setAnalysis(null);
      return;
    }
    if (isDemo) {
      setAnalysis(getMockAnalysis(selectedThreat));
      return;
    }
    setAnalysisLoading(true);
    fetchAnalysisFromApi(selectedThreat.id)
      .then(setAnalysis)
      .catch(() => setAnalysis(getMockAnalysis(selectedThreat)))
      .finally(() => setAnalysisLoading(false));
  }, [selectedThreat, isDemo]);

  const handleMarkReviewed = () => {
    if (selectedThreatId == null) return;
    setReviewedIds((prev) => (prev.includes(selectedThreatId) ? prev : [...prev, selectedThreatId]));
  };

  if (overviewError || threatsError) {
    return (
      <ErrorState
        onRetry={() => {
          retryOverview();
          retryThreats();
        }}
      />
    );
  }

  const isProtected = overview?.status === 'protected';

  return (
    <div className="space-y-5">
      <div className="flex justify-end">
        <ModeToggle />
      </div>

      {/* Overall status banner */}
      {overviewLoading ? (
        <div className="flex items-center gap-3 rounded-lg border border-border bg-surface px-5 py-4">
          <SkeletonBar className="h-9 w-9 rounded-md" />
          <div className="flex-1">
            <SkeletonBar className="mb-2 h-3.5 w-40" />
            <SkeletonBar className="h-3 w-56" />
          </div>
        </div>
      ) : (
        <div
          className={[
            'flex items-center gap-3 rounded-lg border px-5 py-4',
            isProtected ? 'border-safe/25 bg-safe/[0.06]' : 'border-critical/25 bg-critical/[0.06]',
          ].join(' ')}
        >
          <div className={`flex h-9 w-9 items-center justify-center rounded-md ${isProtected ? 'bg-safe/15 text-safe' : 'bg-critical/15 text-critical'}`}>
            <ShieldCheck size={18} />
          </div>
          <div>
            <p className="text-sm font-semibold text-ink">{overview.statusLabel}</p>
            <p className="text-xs text-ink-muted">Last full scan {overview.lastScan}</p>
          </div>
          <div className="ml-auto text-right">
            <p className="text-[11px] uppercase tracking-wide text-ink-muted">Active Threats</p>
            <p className="font-mono text-sm font-semibold text-ink">{overview.threatCount}</p>
          </div>
        </div>
      )}

      {/* Risk score + key stats */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-4">
        {overviewLoading ? (
          <>
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
            <StatCardSkeleton />
          </>
        ) : (
          <>
            <RiskScore
              score={overview.riskScore}
              level={overview.riskLevel}
              trend={overview.riskTrend}
              lastScan={overview.lastScan}
            />
            <StatCard
              icon={Bug}
              label="Active Threats"
              value={overview.threatCount}
              tone={overview.threatCount > 0 ? 'high' : 'safe'}
              hint="Currently being tracked"
            />
            <StatCard
              icon={ListTree}
              label="Security Events"
              value={overview.eventCount24h}
              hint="Logged in the last 24 hours"
            />
            <StatCard
              icon={Siren}
              label="Critical Alerts"
              value={overview.criticalAlerts}
              tone={overview.criticalAlerts > 0 ? 'critical' : 'safe'}
              hint="Requires immediate review"
            />
          </>
        )}
      </div>

      {/* Activity trend + system status */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <ActivityChart data={activityData} />
        </div>
        <SecurityStatus systems={systemStatus} />
      </div>

      {/* Threat distribution + category breakdown */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <RiskDistributionChart data={riskDistribution} />
        <CategoryActivityChart data={categoryActivity} />
      </div>

      {/* Recent threats */}
      <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-semibold text-ink">Recent Threats</p>
            <p className="text-xs text-ink-muted">Most recent detections across this device</p>
          </div>
          <button type="button" className="text-xs font-medium text-accent hover:text-accent/80">
            View all
          </button>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2">
          {threatsLoading ? (
            <>
              <ThreatCardSkeleton />
              <ThreatCardSkeleton />
              <ThreatCardSkeleton />
              <ThreatCardSkeleton />
            </>
          ) : (
            (threats ?? []).map((threat) => (
              <ThreatCard
                key={threat.id}
                threat={threat}
                reviewed={reviewedIds.includes(threat.id)}
                onViewAnalysis={(t) => setSelectedThreatId(t.id)}
              />
            ))
          )}
        </div>
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
          onClose={() => setSelectedThreatId(null)}
          onMarkReviewed={handleMarkReviewed}
        />
      )}
    </div>
  );
}