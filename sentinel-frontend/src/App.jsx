import { useState } from 'react';
import { DemoModeProvider } from './context/DemoModeContext';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import Dashboard from './pages/Dashboard';
import Threats from './pages/Threats';
import Events from './pages/Events';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

const PAGES = {
  dashboard: { component: Dashboard, title: 'Dashboard', subtitle: 'Overview of this device\u2019s security posture' },
  threats: { component: Threats, title: 'Threats', subtitle: 'Detected threats and response actions' },
  events: { component: Events, title: 'Security Events', subtitle: 'Full activity and event log' },
  reports: { component: Reports, title: 'Reports', subtitle: 'Historical security summaries' },
  settings: { component: Settings, title: 'Settings', subtitle: 'Configure Sentinel AI' },
};

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const page = PAGES[activePage] ?? PAGES.dashboard;
  const PageComponent = page.component;

  return (
   <DemoModeProvider>
    <div className="flex h-screen bg-canvas bg-grid bg-[length:28px_28px] text-ink">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar title={page.title} subtitle={page.subtitle} />
        <main className="flex-1 overflow-y-auto p-6">
          <PageComponent />
        </main>
      </div>
    </div>
   </DemoModeProvider>
  );
}
