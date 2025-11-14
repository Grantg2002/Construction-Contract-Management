import { useEffect } from 'react'

function ScopeModal({ subcontract, onClose }) {
  useEffect(() => {
    // Close on Escape key
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }
    document.addEventListener('keydown', handleEscape)
    return () => document.removeEventListener('keydown', handleEscape)
  }, [onClose])

  if (!subcontract) return null

  // Get trade label from scope items or use a default
  const tradeLabel = subcontract.trade_label || subcontract.category || 'General'

  return (
    <div 
      className="fixed inset-0 z-40 flex items-center justify-center bg-slate-900/40 px-4"
      onClick={onClose}
    >
      <div 
        className="w-full max-w-lg rounded-3xl bg-white shadow-xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-5 py-3 border-b border-slate-200 flex items-center justify-between">
          <div>
            <div className="text-[11px] font-medium text-slate-500">Scope of Work</div>
            <div className="text-sm font-semibold text-slate-900">
              {tradeLabel} – {subcontract.company_name}
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-full border border-slate-200 px-2.5 py-1 text-xs text-slate-500 hover:bg-slate-50"
          >
            Close
          </button>
        </div>
        <div className="px-5 py-4 text-xs leading-relaxed text-slate-700 max-h-[60vh] overflow-y-auto">
          {/* Render HTML scope */}
          {subcontract.scope_of_work_html ? (
            <div dangerouslySetInnerHTML={{ __html: subcontract.scope_of_work_html }} />
          ) : (
            <p className="text-slate-500 italic">No scope of work available</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default ScopeModal

