import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

// Use Vite proxy in development, or full URL if specified
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

function UploadProposal() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const projectId = searchParams.get('project')

  useEffect(() => {
    if (!projectId) {
      setError('No project ID provided. Please select a project first.')
    }
  }, [projectId])

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    setResult(null)
    setError(null)
  }

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file')
      return
    }

    if (!projectId) {
      alert('No project selected. Please go back and select a project first.')
      return
    }

    setUploading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('file', file)

      // Call backend API (uses Vite proxy in dev, or full URL if VITE_API_BASE_URL is set)
      const apiUrl = API_BASE_URL || '/api'
      const response = await fetch(`${apiUrl}/projects/${projectId}/proposals`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorData.error || errorMessage
        } catch (e) {
          // If response isn't JSON, try to get text
          const text = await response.text().catch(() => '')
          if (text) errorMessage = text.substring(0, 200)
        }
        throw new Error(errorMessage)
      }

      const data = await response.json()
      
      if (data.success !== false) {
        setResult(data)
        // Optionally navigate to project detail page
        setTimeout(() => {
          navigate(`/project/${projectId}`)
        }, 2000)
      } else {
        throw new Error(data.error || data.detail || 'Upload failed')
      }
    } catch (error) {
      console.error('Upload error:', error)
      const errorMsg = error.message || 'Error uploading proposal. Make sure the backend server is running at http://localhost:8000'
      setError(errorMsg)
      alert(`Error: ${errorMsg}`)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="mb-4 text-xs text-slate-500 hover:text-slate-700 transition"
      >
        ← Back to Dashboard
      </button>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6">
        <h1 className="text-xl font-semibold text-slate-900 mb-6">
          Upload Proposal
        </h1>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-xs text-red-700">{error}</p>
            {error.includes('backend') && (
              <p className="text-[10px] text-red-600 mt-1">
                Make sure the backend server is running: <code className="bg-red-100 px-1 rounded">cd backend && python -m uvicorn main:app --reload</code>
              </p>
            )}
          </div>
        )}

        {!projectId && (
          <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-xs text-yellow-700">
              No project selected. Please go back and select a project first.
            </p>
          </div>
        )}

        <div className="mb-6">
          <label className="block text-xs font-medium text-slate-700 mb-2">
            Select Proposal File
          </label>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.doc,.docx"
            className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200"
          />
          {file && (
            <p className="text-xs text-slate-600 mt-2">
              Selected: <span className="font-medium">{file.name}</span>
            </p>
          )}
        </div>

        <button
          onClick={handleUpload}
          disabled={!file || uploading || !projectId}
          className="w-full bg-slate-900 hover:bg-black disabled:bg-slate-400 text-white px-4 py-2 rounded-lg text-sm font-semibold transition"
        >
          {uploading ? 'Processing...' : 'Upload and Analyze'}
        </button>

        {result && (
          <div className="mt-6 p-4 bg-slate-50 rounded-lg border border-slate-200">
            <h2 className="text-sm font-semibold text-slate-900 mb-3">
              ✓ Proposal Processed Successfully
            </h2>
            <div className="space-y-2 text-xs">
              <p className="text-slate-700">
                <span className="font-medium">Company:</span> {result.extracted_data?.company_name || 'N/A'}
              </p>
              <p className="text-slate-700">
                <span className="font-medium">Total Price:</span> {result.extracted_data?.total_price ? `$${result.extracted_data.total_price.toLocaleString()}` : 'N/A'}
              </p>
              <p className="text-slate-700">
                <span className="font-medium">Scope Items:</span> {result.extracted_data?.scope_items?.length || 0} items extracted
              </p>
              {result.extraction_cost && (
                <p className="text-slate-500">
                  Extraction Cost: ${result.extraction_cost.toFixed(4)}
                </p>
              )}
            </div>
            <p className="text-xs text-slate-500 mt-3">
              Redirecting to project page...
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default UploadProposal

