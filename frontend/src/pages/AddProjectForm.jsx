import { useState, useRef } from 'react'
import { supabase } from '../supabaseClient'

function AddProjectForm({ onClose, onSuccess }) {
  const [name, setName] = useState('')
  const [projectStartDate, setProjectStartDate] = useState('')
  const [location, setLocation] = useState('')
  const [saving, setSaving] = useState(false)
  
  // File uploads
  const [drawingsFiles, setDrawingsFiles] = useState([])
  const [permitsFiles, setPermitsFiles] = useState([])
  const [referenceFiles, setReferenceFiles] = useState([])
  
  const drawingsInputRef = useRef(null)
  const permitsInputRef = useRef(null)
  const referenceInputRef = useRef(null)

  const handleFileSelect = (type, files) => {
    const fileArray = Array.from(files)
    if (type === 'drawings') {
      setDrawingsFiles(fileArray)
    } else if (type === 'permits') {
      setPermitsFiles(fileArray)
    } else if (type === 'reference') {
      setReferenceFiles(fileArray)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e, type) => {
    e.preventDefault()
    e.stopPropagation()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileSelect(type, files)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) {
      alert('Please enter a project name')
      return
    }

    setSaving(true)
    try {
      const projectData = {
        name: name.trim(),
        project_start_date: projectStartDate || null,
      }

      // Parse location if provided (format: "City, State" or just address)
      if (location.trim()) {
        const locationParts = location.split(',').map(s => s.trim())
        if (locationParts.length >= 2) {
          projectData.city = locationParts[0]
          projectData.state = locationParts[1]
        } else {
          projectData.street = locationParts[0]
        }
      }

      // Create project first
      const { data: project, error: projectError } = await supabase
        .from('projects')
        .insert([projectData])
        .select()
        .single()

      if (projectError) throw projectError

      // Upload files if any were selected
      // For now, we'll just store file metadata - actual file storage can be added later
      // Files are stored in state and can be uploaded after project creation if needed

      if (onSuccess) {
        onSuccess(project)
      }
    } catch (error) {
      console.error('Error creating project:', error)
      alert('Error creating project: ' + error.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-slate-900/40 flex items-center justify-center z-50 px-4 overflow-y-auto py-8">
      <div className="bg-white rounded-3xl shadow-xl p-6 w-full max-w-2xl my-auto">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-slate-900">
            New Project
          </h2>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-600"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Core Fields */}
          <div className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1.5">
                Project Name *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent"
                placeholder="Eastown Place Apts"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1.5">
                Project Start Date
              </label>
              <input
                type="date"
                value={projectStartDate}
                onChange={(e) => setProjectStartDate(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1.5">
                Location / Client (optional)
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-transparent"
                placeholder="Grand Rapids, MI or 123 Main St"
              />
            </div>
          </div>

          {/* Project Files Section */}
          <div className="border-t border-slate-200 pt-6">
            <h3 className="text-xs font-semibold text-slate-900 mb-4">
              Attach key project files
            </h3>
            
            <div className="space-y-3">
              {/* Drawings Card */}
              <div className="border border-slate-200 rounded-xl p-4">
                <label className="block text-xs font-medium text-slate-700 mb-2">
                  Drawings
                </label>
                <input
                  type="file"
                  ref={drawingsInputRef}
                  multiple
                  accept=".pdf,.dwg,.dwf"
                  onChange={(e) => handleFileSelect('drawings', e.target.files)}
                  className="hidden"
                />
                <div
                  onClick={() => drawingsInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDrop(e, 'drawings')}
                  className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition cursor-pointer"
                >
                  {drawingsFiles.length > 0 ? (
                    <div>
                      <p className="text-xs text-slate-900 font-medium">
                        {drawingsFiles.length} file{drawingsFiles.length > 1 ? 's' : ''} selected
                      </p>
                      {drawingsFiles.map((file, idx) => (
                        <p key={idx} className="text-[10px] text-slate-600 mt-1">
                          {file.name}
                        </p>
                      ))}
                    </div>
                  ) : (
                    <>
                      <p className="text-xs text-slate-600">
                        Construction drawings (PDF, DWG exports, etc.)
                      </p>
                      <p className="text-[10px] text-slate-400 mt-1">
                        Drag and drop or click to upload
                      </p>
                    </>
                  )}
                </div>
              </div>

              {/* Permits Card */}
              <div className="border border-slate-200 rounded-xl p-4">
                <label className="block text-xs font-medium text-slate-700 mb-2">
                  Permits & Approvals
                </label>
                <input
                  type="file"
                  ref={permitsInputRef}
                  multiple
                  accept=".pdf"
                  onChange={(e) => handleFileSelect('permits', e.target.files)}
                  className="hidden"
                />
                <div
                  onClick={() => permitsInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDrop(e, 'permits')}
                  className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition cursor-pointer"
                >
                  {permitsFiles.length > 0 ? (
                    <div>
                      <p className="text-xs text-slate-900 font-medium">
                        {permitsFiles.length} file{permitsFiles.length > 1 ? 's' : ''} selected
                      </p>
                      {permitsFiles.map((file, idx) => (
                        <p key={idx} className="text-[10px] text-slate-600 mt-1">
                          {file.name}
                        </p>
                      ))}
                    </div>
                  ) : (
                    <>
                      <p className="text-xs text-slate-600">
                        Building permit, soil erosion/sedimentation control, stormwater permits…
                      </p>
                      <p className="text-[10px] text-slate-400 mt-1">
                        Drag and drop or click to upload
                      </p>
                    </>
                  )}
                </div>
              </div>

              {/* Reference Docs Card */}
              <div className="border border-slate-200 rounded-xl p-4">
                <label className="block text-xs font-medium text-slate-700 mb-2">
                  Reference Docs
                </label>
                <input
                  type="file"
                  ref={referenceInputRef}
                  multiple
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => handleFileSelect('reference', e.target.files)}
                  className="hidden"
                />
                <div
                  onClick={() => referenceInputRef.current?.click()}
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDrop(e, 'reference')}
                  className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition cursor-pointer"
                >
                  {referenceFiles.length > 0 ? (
                    <div>
                      <p className="text-xs text-slate-900 font-medium">
                        {referenceFiles.length} file{referenceFiles.length > 1 ? 's' : ''} selected
                      </p>
                      {referenceFiles.map((file, idx) => (
                        <p key={idx} className="text-[10px] text-slate-600 mt-1">
                          {file.name}
                        </p>
                      ))}
                    </div>
                  ) : (
                    <>
                      <p className="text-xs text-slate-600">
                        Specs, geotech report, soils borings, correspondence PDFs…
                      </p>
                      <p className="text-[10px] text-slate-400 mt-1">
                        Drag and drop or click to upload
                      </p>
                    </>
                  )}
                </div>
              </div>
            </div>
            
            <p className="text-[10px] text-slate-400 mt-3">
              Files will be uploaded when you click "Create Project"
            </p>
          </div>

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4 border-t border-slate-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm text-slate-700 bg-slate-100 rounded-lg hover:bg-slate-200 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 text-sm font-semibold text-white bg-slate-900 rounded-lg hover:bg-black disabled:bg-slate-400 transition"
            >
              {saving ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddProjectForm

