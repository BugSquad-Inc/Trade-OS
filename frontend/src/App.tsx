import React, { useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AppShell } from './components/layout/AppShell';
import { TodayCockpitView } from './components/today/TodayCockpitView';
import { SalesHubView } from './components/sales/SalesHubView';
import { OrdersHubView } from './components/orders/OrdersHubView';
import { MoneyHubView } from './components/money/MoneyHubView';
import { MyBusinessHubView } from './components/business/MyBusinessHubView';

// Backstage / Expert Views
import { DealsPipelineView } from './components/deals/DealsPipelineView';
import { MatchPortalView } from './components/matches/MatchPortalView';
import { SignalsView } from './components/signals/SignalsView';
import { Account360View } from './components/accounts/Account360View';
import { ProductPassportView } from './components/products/ProductPassportView';
import { DocumentPackView } from './components/documents/DocumentPackView';
import { ShipmentMilestoneTrackerView } from './components/shipments/ShipmentMilestoneTrackerView';
import { VerificationQueueView } from './components/verification/VerificationQueueView';
import { CustomsExplorerView } from './components/customs/CustomsExplorerView';
import { ExecutiveDashboardView } from './components/analytics/ExecutiveDashboardView';
import { AuditTrailView } from './components/audit/AuditTrailView';

// Modals
import { OnboardingWizardModal } from './components/onboarding/OnboardingWizardModal';
import { TeamManagementModal } from './components/tenants/TeamManagementModal';
import { ExportGlossaryModal } from './components/ui/ExportGlossaryModal';
import { CommandPaletteModal } from './components/ui/CommandPaletteModal';
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
  const { 
    currentView, 
    setCurrentView,
    isOnboardingModalOpen, 
    setOnboardingModalOpen, 
    isTeamModalOpen, 
    setTeamModalOpen,
    setCommandPaletteOpen,
    setGlossaryModalOpen
  } = useUIStore();

  // Global Keyboard Shortcuts (Cmd+K, 1-5, ?)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if user is currently typing in an input or textarea
      const target = e.target as HTMLElement;
      if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable) {
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
          e.preventDefault();
          setCommandPaletteOpen(true);
        }
        return;
      }

      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      } else if (e.key === '1') {
        e.preventDefault();
        setCurrentView('today');
      } else if (e.key === '2') {
        e.preventDefault();
        setCurrentView('sales');
      } else if (e.key === '3') {
        e.preventDefault();
        setCurrentView('orders');
      } else if (e.key === '4') {
        e.preventDefault();
        setCurrentView('money');
      } else if (e.key === '5') {
        e.preventDefault();
        setCurrentView('business');
      } else if (e.key === '?') {
        e.preventDefault();
        setGlossaryModalOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [setCurrentView, setCommandPaletteOpen, setGlossaryModalOpen]);

  return (
    <AppShell>
      <ErrorBoundary>
        {/* Primary 5 Owner Jobs */}
        {currentView === 'today' && <TodayCockpitView />}
        {currentView === 'sales' && <SalesHubView />}
        {currentView === 'orders' && <OrdersHubView />}
        {currentView === 'money' && <MoneyHubView />}
        {currentView === 'business' && <MyBusinessHubView />}

        {/* Backstage / Direct Views */}
        {currentView === 'deals' && <DealsPipelineView />}
        {currentView === 'matches' && <MatchPortalView />}
        {currentView === 'signals' && <SignalsView />}
        {currentView === 'accounts' && <Account360View />}
        {currentView === 'products' && <ProductPassportView />}
        {currentView === 'documents' && <DocumentPackView />}
        {currentView === 'shipments' && <ShipmentMilestoneTrackerView />}
        {currentView === 'verification' && <VerificationQueueView />}
        {currentView === 'customs' && <CustomsExplorerView />}
        {currentView === 'analytics' && <ExecutiveDashboardView />}
        {currentView === 'audit' && <AuditTrailView />}
      </ErrorBoundary>

      <OnboardingWizardModal
        isOpen={isOnboardingModalOpen}
        onClose={() => setOnboardingModalOpen(false)}
      />

      <TeamManagementModal
        isOpen={isTeamModalOpen}
        onClose={() => setTeamModalOpen(false)}
      />

      <ExportGlossaryModal />
      <CommandPaletteModal />
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
