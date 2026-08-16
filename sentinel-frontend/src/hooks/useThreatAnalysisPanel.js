import { useEffect, useState } from 'react';
import { useDemoMode } from '../context/DemoModeContext';
import { getThreatAnalysis as fetchAnalysisFromApi } from '../services/api';
import { getThreatAnalysis as getMockAnalysis } from '../data/mockData';

// Shared "View Analysis" panel logic — used by Dashboard, Threats, and
// Events pages so all three open the same AI Explanation panel the same way,
// instead of each page re-implementing this state.
export function useThreatAnalysisPanel(threats) {
  const { isDemo } = useDemoMode();
  const [selectedThreatId, setSelectedThreatId] = useState(null);
  const [reviewedIds, setReviewedIds] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const selectedThreat = (threats ?? []).find((t) => t.id === selectedThreatId) ?? null;

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

  return {
    selectedThreat,
    analysis,
    analysisLoading,
    reviewedIds,
    openThreat: (t) => setSelectedThreatId(t.id),
    closeThreat: () => setSelectedThreatId(null),
    handleMarkReviewed,
  };
}