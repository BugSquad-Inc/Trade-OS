import React from 'react';
import { GlassSidebar } from './GlassSidebar';
import { GlassTopbar } from './GlassTopbar';
import { AppleCommandBar } from '../apple/AppleCommandBar';
import { useUIStore } from '../../store/uiStore';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const { isCommandBarOpen, setCommandBarOpen, setSelectedBuyerId, setCurrentView } = useUIStore();

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-zinc-950 text-zinc-100">
      {/* Sidebar */}
      <GlassSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        <GlassTopbar />
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>

      {/* Global Spotlight Palette */}
      <AppleCommandBar
        isOpen={isCommandBarOpen}
        onClose={() => setCommandBarOpen(false)}
        onSelectBuyer={(id) => {
          setSelectedBuyerId(id);
          setCurrentView('accounts');
        }}
        onNavigate={(view) => setCurrentView(view)}
      />
    </div>
  );
};
