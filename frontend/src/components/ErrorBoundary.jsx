import React from 'react'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
          <div className="max-w-md w-full bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
            <h1 className="text-lg font-semibold text-slate-900 mb-2">
              Application Error
            </h1>
            <p className="text-sm text-slate-600 mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <div className="bg-slate-50 rounded-lg p-3 mb-4">
              <p className="text-xs text-slate-500 font-mono">
                {this.state.error?.stack}
              </p>
            </div>
            <button
              onClick={() => window.location.reload()}
              className="w-full px-4 py-2 text-sm font-semibold text-white bg-slate-900 rounded-lg hover:bg-black"
            >
              Reload Page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary

