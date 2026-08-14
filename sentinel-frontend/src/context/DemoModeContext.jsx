import { createContext, useContext, useState } from 'react';

const DemoModeContext = createContext(null);

export function DemoModeProvider({ children }) {
  // Starts in demo mode so the app always works, even with zero backend running.
  const [mode, setMode] = useState('demo'); // 'demo' | 'live'
  const toggleMode = () => setMode((m) => (m === 'demo' ? 'live' : 'demo'));

  return (
    <DemoModeContext.Provider value={{ mode, isDemo: mode === 'demo', toggleMode }}>
      {children}
    </DemoModeContext.Provider>
  );
}

export function useDemoMode() {
  const ctx = useContext(DemoModeContext);
  if (!ctx) throw new Error('useDemoMode must be used within DemoModeProvider');
  return ctx;
}