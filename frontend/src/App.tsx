import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { TodayCockpitView } from './components/today/TodayCockpitView';
import { DealsPipelineView } from './components/deals/DealsPipelineView';
import { MatchPortalView } from './components/matches/MatchPortalView';
import { SignalsView } from './components/signals/SignalsView';
import { Account360View } from './components/accounts/Account360View';
import { ProductPassportView } from './components/products/ProductPassportView';
import { VerificationQueueView } from './components/verification/VerificationQueueView';
import { CustomsExplorerView } from './components/customs/CustomsExplorerView';
import { ExecutiveDashboardView } from './components/analytics/ExecutiveDashboardView';
import { OnboardingWizardModal } from './components/onboarding/OnboardingWizardModal';
import { TeamManagementModal } from './components/tenants/TeamManagementModal';
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
  const { currentView, isOnboardingModalOpen, setOnboardingModalOpen, isTeamModalOpen, setTeamModalOpen } = useUIStore();

  return (
    <AppShell>
      <ErrorBoundary>
        {currentView === 'today' && <TodayCockpitView />}
        {currentView === 'deals' && <DealsPipelineView />}
        {currentView === 'matches' && <MatchPortalView />}
        {currentView === 'signals' && <SignalsView />}
        {currentView === 'accounts' && <Account360View />}
        {currentView === 'products' && <ProductPassportView />}
        {currentView === 'verification' && <VerificationQueueView />}
        {currentView === 'customs' && <CustomsExplorerView />}
        {currentView === 'analytics' && <ExecutiveDashboardView />}
      </ErrorBoundary>

      <OnboardingWizardModal
        isOpen={isOnboardingModalOpen}
        onClose={() => setOnboardingModalOpen(false)}
      />

      <TeamManagementModal
        isOpen={isTeamModalOpen}
        onClose={() => setTeamModalOpen(false)}
      />
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
