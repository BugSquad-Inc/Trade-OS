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
        <div className="min-h-[400px] flex flex-col items-center justify-center p-8 text-center bg-white rounded-3xl border border-rose-200 shadow-md m-6">
          <div className="p-4 bg-rose-50 rounded-full text-rose-600 mb-4">
            <AlertTriangle size={32} />
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">Something went wrong</h2>
          <p className="text-sm text-slate-500 max-w-md mb-6">
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
