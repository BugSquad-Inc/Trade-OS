import React from 'react';
import { GlassSidebar } from './GlassSidebar';
import { GlassTopbar } from './GlassTopbar';
import { MobileBottomNav } from './MobileBottomNav';
import { AppleCommandBar } from '../apple/AppleCommandBar';
import { useUIStore } from '../../store/uiStore';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  const { isCommandBarOpen, setCommandBarOpen, setSelectedBuyerId, setCurrentView } = useUIStore();

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#F5F5F7] text-slate-900 font-sans">
      {/* Translucent Silver/White Sidebar (Responsive desktop fixed / mobile off-canvas drawer) */}
      <GlassSidebar />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden min-w-0">
        <GlassTopbar />
        
        {/* Main scrollable viewport with bottom nav clearance on mobile */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 bg-[#F5F5F7] pb-24 md:pb-8">
          <div className="max-w-7xl mx-auto w-full">
            {children}
          </div>
        </main>
      </div>

      {/* Mobile Bottom Navigation (Visible on screen < 768px) */}
      <MobileBottomNav />

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
