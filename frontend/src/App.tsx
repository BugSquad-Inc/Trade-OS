import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { MatchPortalView } from './components/matches/MatchPortalView';
import { SignalsView } from './components/signals/SignalsView';
import { Account360View } from './components/accounts/Account360View';
import { CustomsExplorerView } from './components/customs/CustomsExplorerView';
import { ExecutiveDashboardView } from './components/analytics/ExecutiveDashboardView';
import { ErrorBoundary } from './components/ui/ErrorBoundary';
import { useUIStore } from './store/uiStore';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,
      refetchOnWindowFocus: false,
    },
  },
});

function AppContent() {
  const { currentView } = useUIStore();

  return (
    <AppShell>
      <ErrorBoundary>
        {currentView === 'matches' && <MatchPortalView />}
        {currentView === 'signals' && <SignalsView />}
        {currentView === 'accounts' && <Account360View />}
        {currentView === 'customs' && <CustomsExplorerView />}
        {currentView === 'analytics' && <ExecutiveDashboardView />}
      </ErrorBoundary>
    </AppShell>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}
