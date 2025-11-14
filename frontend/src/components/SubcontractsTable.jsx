import { useState } from 'react'
import ScopeModal from './ScopeModal'

function formatCurrency(value) {
  if (!value) return '$0'
  return value.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  })
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

function SubcontractsTable({ subcontracts, loading }) {
  const [selectedScope, setSelectedScope] = useState(null)
  const [downloading, setDownloading] = useState(null)

  const handleDownload = async (subcontractId) => {
    setDownloading(subcontractId)
    try {
      const apiUrl = import.meta.env.VITE_API_BASE_URL || '/api'
      const response = await fetch(`${apiUrl}/subcontracts/${subcontractId}/download-contract`)
      
      if (!response.ok) {
        throw new Error('Failed to download contract')
      }
      
      // Get filename from Content-Disposition header or use default
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'contract.docx'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }
      
      // Create blob and download
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Download error:', error)
      alert('Error downloading contract: ' + error.message)
    } finally {
      setDownloading(null)
    }
  }

  if (loading) {
    return (
      <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-8 text-center">
        <p className="text-slate-500">Loading subcontracts...</p>
      </div>
    )
  }

  if (!subcontracts || subcontracts.length === 0) {
    return (
      <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-8 text-center">
        <p className="text-slate-500">No subcontracts yet</p>
      </div>
    )
  }

  return (
    <>
      <div className="mt-4 rounded-2xl border border-slate-200 bg-white overflow-hidden">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="text-xs uppercase tracking-wide text-slate-500 border-b border-slate-200 bg-slate-50">
              <th className="text-left px-4 py-2 font-medium">Subcontractor</th>
              <th className="text-left px-4 py-2 font-medium">Created</th>
              <th className="text-left px-4 py-2 font-medium">Trade / Scope</th>
              <th className="text-right px-4 py-2 font-medium">Contract Value</th>
              <th className="text-right px-4 py-2 font-medium">Amount Invoiced</th>
              <th className="text-left px-4 py-2 font-medium">% Billed</th>
              <th className="text-center px-4 py-2 font-medium">Download</th>
            </tr>
          </thead>
          <tbody>
            {subcontracts.map((sc) => {
              const contractValue = parseFloat(sc.current_amount || sc.original_amount || 0)
              const amountInvoiced = parseFloat(sc.total_billed || 0)
              const percent = contractValue > 0
                ? Math.min(100, Math.round((amountInvoiced / contractValue) * 100))
                : 0

              // Get trade label from scope items or use company name
              const tradeLabel = sc.scope_summary || sc.company_name || 'General'

              return (
                <tr
                  key={sc.id}
                  className="border-b border-slate-100 hover:bg-slate-50/70 transition"
                >
                  <td className="px-4 py-2 text-slate-900">{sc.company_name || 'N/A'}</td>
                  <td className="px-4 py-2 text-slate-600 text-xs">
                    {formatDate(sc.created_at)}
                  </td>
                  <td className="px-4 py-2">
                    {sc.scope_of_work_html ? (
                      <button
                        onClick={() => setSelectedScope(sc)}
                        className="text-xs inline-flex items-center gap-1 rounded-full px-3 py-1 bg-slate-100 text-slate-700 hover:bg-slate-200 transition"
                      >
                        {tradeLabel}
                        <span className="text-[10px] text-slate-500">View scope</span>
                      </button>
                    ) : (
                      <span className="text-xs text-slate-500">{tradeLabel}</span>
                    )}
                  </td>
                  <td className="px-4 py-2 text-right text-slate-900">
                    {formatCurrency(contractValue)}
                  </td>
                  <td className="px-4 py-2 text-right text-slate-700">
                    {formatCurrency(amountInvoiced)}
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 rounded-full bg-slate-100 overflow-hidden">
                        <div
                          className="h-full rounded-full bg-slate-900 transition-all"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                      <span className="text-xs text-slate-700 w-10 text-right">
                        {percent}%
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-2 text-center">
                    <button
                      onClick={() => handleDownload(sc.id)}
                      disabled={downloading === sc.id}
                      className="text-xs inline-flex items-center gap-1 rounded-full px-3 py-1 bg-slate-900 text-white hover:bg-black disabled:bg-slate-400 disabled:cursor-not-allowed transition"
                      title="Download Word document"
                    >
                      {downloading === sc.id ? (
                        <>
                          <span className="animate-spin">⏳</span>
                          <span>Generating...</span>
                        </>
                      ) : (
                        <>
                          <span>📥</span>
                          <span>Download</span>
                        </>
                      )}
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <ScopeModal
        subcontract={selectedScope}
        onClose={() => setSelectedScope(null)}
      />
    </>
  )
}

export default SubcontractsTable

