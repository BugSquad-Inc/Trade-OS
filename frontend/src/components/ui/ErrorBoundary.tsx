import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { AppleButton } from '../apple/AppleButton';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex flex-col items-center justify-center p-8 text-center bg-zinc-900/50 rounded-2xl border border-rose-500/20 m-6">
          <div className="p-4 bg-rose-500/10 rounded-full text-rose-400 mb-4">
            <AlertTriangle size={32} />
          </div>
          <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>
          <p className="text-sm text-zinc-400 max-w-md mb-6">
            {this.state.error?.message || 'An unexpected rendering error occurred in this view.'}
          </p>
          <AppleButton
            variant="secondary"
            icon={<RefreshCw size={16} />}
            onClick={() => this.setState({ hasError: false })}
          >
            Retry Component
          </AppleButton>
        </div>
      );
    }
    return this.props.children;
  }
}
