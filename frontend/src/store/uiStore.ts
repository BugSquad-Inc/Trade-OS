import { create } from 'zustand';

export type AppView = 'today' | 'deals' | 'matches' | 'signals' | 'accounts' | 'products' | 'customs' | 'analytics' | 'verification';

interface UIState {
  currentView: AppView;
  selectedBuyerId: string | null;
  selectedInspectorMatch: any | null;
  isCommandBarOpen: boolean;
  isInspectorOpen: boolean;
  isSimpleMode: boolean;
  isMobileDrawerOpen: boolean;
  isOnboardingModalOpen: boolean;
  
  setCurrentView: (view: AppView) => void;
  setSelectedBuyerId: (id: string | null) => void;
  setSelectedInspectorMatch: (match: any | null) => void;
  setCommandBarOpen: (open: boolean) => void;
  setInspectorOpen: (open: boolean) => void;
  setSimpleMode: (simple: boolean) => void;
  toggleSimpleMode: () => void;
  setMobileDrawerOpen: (open: boolean) => void;
  setOnboardingModalOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentView: 'today',
  selectedBuyerId: null,
  selectedInspectorMatch: null,
  isCommandBarOpen: false,
  isInspectorOpen: false,
  isSimpleMode: true, // Default to Simple Mode for SMB owners
  isMobileDrawerOpen: false,
  isOnboardingModalOpen: false,

  setCurrentView: (view) => set({ currentView: view, isMobileDrawerOpen: false }),
  setSelectedBuyerId: (id) => set({ selectedBuyerId: id }),
  setSelectedInspectorMatch: (match) => set({ selectedInspectorMatch: match, isInspectorOpen: !!match }),
  setCommandBarOpen: (open) => set({ isCommandBarOpen: open }),
  setInspectorOpen: (open) => set({ isInspectorOpen: open }),
  setSimpleMode: (simple) => set({ isSimpleMode: simple }),
  toggleSimpleMode: () => set((state) => ({ isSimpleMode: !state.isSimpleMode })),
  setMobileDrawerOpen: (open) => set({ isMobileDrawerOpen: open }),
  setOnboardingModalOpen: (open) => set({ isOnboardingModalOpen: open }),
}));
