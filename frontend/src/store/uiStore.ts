import { create } from 'zustand';

export type AppView = 
  | 'today' 
  | 'sales' 
  | 'orders' 
  | 'money' 
  | 'business'
  // Legacy / Direct deep link views
  | 'deals' 
  | 'matches' 
  | 'signals' 
  | 'accounts' 
  | 'products' 
  | 'documents' 
  | 'shipments' 
  | 'customs' 
  | 'analytics' 
  | 'verification' 
  | 'audit';

export type WorkspaceMode = 'owner' | 'expert';

export type SalesSubTab = 'matches' | 'signals' | 'accounts' | 'quotes';
export type OrdersSubTab = 'deals' | 'documents' | 'shipments' | 'customs';
export type MoneySubTab = 'invoices' | 'realization' | 'margins' | 'analytics';
export type BusinessSubTab = 'profile' | 'products' | 'verification' | 'team' | 'audit';

interface UIState {
  currentView: AppView;
  workspaceMode: WorkspaceMode;
  salesSubTab: SalesSubTab;
  ordersSubTab: OrdersSubTab;
  moneySubTab: MoneySubTab;
  businessSubTab: BusinessSubTab;

  selectedBuyerId: string | null;
  selectedInspectorMatch: any | null;
  isCommandBarOpen: boolean;
  isInspectorOpen: boolean;
  isSimpleMode: boolean;
  isMobileDrawerOpen: boolean;
  isOnboardingModalOpen: boolean;
  isTeamModalOpen: boolean;
  isGlossaryModalOpen: boolean;
  activeGlossaryTerm: string | null;
  
  setCurrentView: (view: AppView) => void;
  setWorkspaceMode: (mode: WorkspaceMode) => void;
  toggleWorkspaceMode: () => void;
  setSalesSubTab: (tab: SalesSubTab) => void;
  setOrdersSubTab: (tab: OrdersSubTab) => void;
  setMoneySubTab: (tab: MoneySubTab) => void;
  setBusinessSubTab: (tab: BusinessSubTab) => void;

  setSelectedBuyerId: (id: string | null) => void;
  setSelectedInspectorMatch: (match: any | null) => void;
  setCommandBarOpen: (open: boolean) => void;
  setInspectorOpen: (open: boolean) => void;
  setSimpleMode: (simple: boolean) => void;
  toggleSimpleMode: () => void;
  setMobileDrawerOpen: (open: boolean) => void;
  setOnboardingModalOpen: (open: boolean) => void;
  setTeamModalOpen: (open: boolean) => void;
  setGlossaryModalOpen: (open: boolean) => void;
  openGlossary: (term?: string) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentView: 'today',
  workspaceMode: 'owner', // Default to Owner Workspace
  salesSubTab: 'matches',
  ordersSubTab: 'deals',
  moneySubTab: 'invoices',
  businessSubTab: 'profile',

  selectedBuyerId: null,
  selectedInspectorMatch: null,
  isCommandBarOpen: false,
  isInspectorOpen: false,
  isSimpleMode: true,
  isMobileDrawerOpen: false,
  isOnboardingModalOpen: false,
  isTeamModalOpen: false,
  isGlossaryModalOpen: false,
  activeGlossaryTerm: null,

  setCurrentView: (view) => set({ currentView: view, isMobileDrawerOpen: false }),
  setWorkspaceMode: (mode) => set({ workspaceMode: mode }),
  toggleWorkspaceMode: () => set((state) => ({ 
    workspaceMode: state.workspaceMode === 'owner' ? 'expert' : 'owner' 
  })),
  setSalesSubTab: (tab) => set({ salesSubTab: tab, currentView: 'sales' }),
  setOrdersSubTab: (tab) => set({ ordersSubTab: tab, currentView: 'orders' }),
  setMoneySubTab: (tab) => set({ moneySubTab: tab, currentView: 'money' }),
  setBusinessSubTab: (tab) => set({ businessSubTab: tab, currentView: 'business' }),

  setSelectedBuyerId: (id) => set({ selectedBuyerId: id }),
  setSelectedInspectorMatch: (match) => set({ selectedInspectorMatch: match, isInspectorOpen: !!match }),
  setCommandBarOpen: (open) => set({ isCommandBarOpen: open }),
  setInspectorOpen: (open) => set({ isInspectorOpen: open }),
  setSimpleMode: (simple) => set({ isSimpleMode: simple }),
  toggleSimpleMode: () => set((state) => ({ isSimpleMode: !state.isSimpleMode })),
  setMobileDrawerOpen: (open) => set({ isMobileDrawerOpen: open }),
  setOnboardingModalOpen: (open) => set({ isOnboardingModalOpen: open }),
  setTeamModalOpen: (open) => set({ isTeamModalOpen: open }),
  setGlossaryModalOpen: (open) => set({ isGlossaryModalOpen: open }),
  openGlossary: (term) => set({ isGlossaryModalOpen: true, activeGlossaryTerm: term || null }),
}));
