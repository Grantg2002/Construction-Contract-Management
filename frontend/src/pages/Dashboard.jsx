import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabaseClient'
import AddProjectForm from './AddProjectForm'
import ProjectCard from '../components/ProjectCard'

function Dashboard() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAddForm, setShowAddForm] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      // Fetch projects with counts
      const { data: projectsData, error: projectsError } = await supabase
        .from('projects')
        .select('*')
        .order('created_at', { ascending: false })

      if (projectsError) throw projectsError

      // Fetch subcontract counts for each project
      const projectsWithCounts = await Promise.all(
        (projectsData || []).map(async (project) => {
          const { count: subcontractsCount, error: scError } = await supabase
            .from('subcontracts')
            .select('*', { count: 'exact', head: true })
            .eq('project_id', project.id)

          const { count: drawingsCount, error: dwgError } = await supabase
            .from('drawings')
            .select('*', { count: 'exact', head: true })
            .eq('project_id', project.id)

          return {
            ...project,
            subcontracts_count: subcontractsCount || 0,
            files_count: drawingsCount || 0
          }
        })
      )

      setProjects(projectsWithCounts)
    } catch (error) {
      console.error('Error fetching projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleProjectClick = (projectId) => {
    navigate(`/project/${projectId}`)
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-slate-500">Loading projects...</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Top bar */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Construction Contract Management</h1>
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowAddForm(true)}
            className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-black transition"
          >
            New Project
          </button>
          <div className="w-8 h-8 rounded-full bg-slate-200"></div>
        </div>
      </div>

      {/* Project grid */}
      {projects.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-2xl border border-slate-200">
          <p className="text-slate-500 mb-4">No projects yet</p>
          <button
            onClick={() => setShowAddForm(true)}
            className="rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-black transition"
          >
            Create your first project
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onOpen={handleProjectClick}
            />
          ))}
        </div>
      )}

      {showAddForm && (
        <AddProjectForm
          onClose={() => setShowAddForm(false)}
          onSuccess={() => {
            setShowAddForm(false)
            fetchProjects()
          }}
        />
      )}
    </div>
  )
}

export default Dashboard

