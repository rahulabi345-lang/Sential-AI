import { useCallback, useEffect, useState } from 'react';
import { useDemoMode } from '../context/DemoModeContext';

export function useApiResource(fetchFn, mockValue, { pollInterval } = {}) {
  const { isDemo } = useDemoMode();
  const [state, setState] = useState({ data: null, loading: true, error: null });

  const load = useCallback(() => {
    if (isDemo) {
      setState({ data: mockValue, loading: false, error: null });
      return;
    }
    setState((s) => ({ ...s, loading: true, error: null }));
    fetchFn()
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((error) => setState({ data: null, loading: false, error }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isDemo]);

  useEffect(() => {
    load();
    if (!isDemo && pollInterval) {
      const id = setInterval(load, pollInterval);
      return () => clearInterval(id);
    }
  }, [load, isDemo, pollInterval]);

  return { ...state, retry: load };
}