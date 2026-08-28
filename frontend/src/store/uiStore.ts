import { create } from 'zustand';

interface UIState {
  currentView: 'matches' | 'signals' | 'accounts';
  selectedBuyerId: string | null;
  selectedInspectorMatch: any | null;
  isCommandBarOpen: boolean;
  isInspectorOpen: boolean;
  setCurrentView: (view: 'matches' | 'signals' | 'accounts') => void;
  setSelectedBuyerId: (id: string | null) => void;
  setSelectedInspectorMatch: (match: any | null) => void;
  setCommandBarOpen: (open: boolean) => void;
  setInspectorOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentView: 'matches',
  selectedBuyerId: null,
  selectedInspectorMatch: null,
  isCommandBarOpen: false,
  isInspectorOpen: false,
  setCurrentView: (view) => set({ currentView: view }),
  setSelectedBuyerId: (id) => set({ selectedBuyerId: id }),
  setSelectedInspectorMatch: (match) => set({ selectedInspectorMatch: match, isInspectorOpen: !!match }),
  setCommandBarOpen: (open) => set({ isCommandBarOpen: open }),
  setInspectorOpen: (open) => set({ isInspectorOpen: open }),
}));
