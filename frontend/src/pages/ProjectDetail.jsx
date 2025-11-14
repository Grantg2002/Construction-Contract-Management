import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { supabase } from '../supabaseClient'
import ProjectHeader from '../components/ProjectHeader'
import SubcontractsTable from '../components/SubcontractsTable'

function ProjectDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [project, setProject] = useState(null)
  const [subcontracts, setSubcontracts] = useState([])
  const [loading, setLoading] = useState(true)
  const [subcontractsLoading, setSubcontractsLoading] = useState(true)

  useEffect(() => {
    fetchProject()
    fetchSubcontracts()
  }, [id])

  const fetchProject = async () => {
    try {
      const { data, error } = await supabase
        .from('projects')
        .select('*')
        .eq('id', id)
        .single()

      if (error) throw error

      // Get counts
      const { count: subcontractsCount } = await supabase
        .from('subcontracts')
        .select('*', { count: 'exact', head: true })
        .eq('project_id', id)

      setProject({
        ...data,
        subcontracts_count: subcontractsCount || 0
      })
    } catch (error) {
      console.error('Error fetching project:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchSubcontracts = async () => {
    try {
      setSubcontractsLoading(true)
      const { data, error } = await supabase
        .from('subcontracts')
        .select('*')
        .eq('project_id', id)
        .order('created_at', { ascending: false })

      if (error) throw error
      setSubcontracts(data || [])
    } catch (error) {
      console.error('Error fetching subcontracts:', error)
    } finally {
      setSubcontractsLoading(false)
    }
  }

  const handleUploadProposalsClick = () => {
    // Navigate to upload proposal page with project ID
    navigate(`/upload-proposal?project=${id}`)
  }

  const handleFilesClick = () => {
    // TODO: Implement files view
    console.log('Files clicked')
  }

  const handlePermitsClick = () => {
    // TODO: Implement permits view
    console.log('Permits clicked')
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-500">Loading project...</p>
      </div>
    )
  }

  if (!project) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-500">Project not found</p>
        <button
          onClick={() => navigate('/')}
          className="mt-4 text-slate-600 hover:text-slate-900"
        >
          ← Back to Dashboard
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <button
        onClick={() => navigate('/')}
        className="mb-4 text-xs text-slate-500 hover:text-slate-700 transition"
      >
        ← Back to Dashboard
      </button>

      {/* Project Header - Tab/Folder Style */}
      <ProjectHeader
        project={project}
        onUploadProposalsClick={handleUploadProposalsClick}
        onFilesClick={handleFilesClick}
        onPermitsClick={handlePermitsClick}
      />

      {/* Main Content Tabs */}
      <div className="mt-6">
        {/* Subcontracts Tab (default) */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900">Subcontracts</h2>
          </div>
          <SubcontractsTable 
            subcontracts={subcontracts} 
            loading={subcontractsLoading}
          />
        </div>
      </div>
    </div>
  )
}

export default ProjectDetail

