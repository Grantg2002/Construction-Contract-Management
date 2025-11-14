function ProjectCard({ project, onOpen }) {
  // Format project start date
  const startDate = project.project_start_date 
    ? new Date(project.project_start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : new Date(project.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })

  // Format location
  const location = project.city && project.state 
    ? `${project.city}, ${project.state}`
    : project.street || 'No location'

  // Get status (default to active)
  const status = project.status || 'active'

  return (
    <button
      onClick={() => onOpen(project.id)}
      className="w-full text-left rounded-2xl border border-slate-200 bg-white px-4 py-4 shadow-sm hover:shadow-md hover:border-slate-300 transition flex flex-col gap-2"
    >
      <div className="flex items-center justify-between gap-2">
        <h2 className="text-sm font-semibold text-slate-900 truncate">
          {project.name}
        </h2>
        <span className="text-[11px] inline-flex items-center px-2 py-0.5 rounded-full bg-slate-900 text-white">
          {status}
        </span>
      </div>
      <div className="text-xs text-slate-500">
        Start:{" "}
        <span className="font-medium text-slate-700">
          {startDate}
        </span>
      </div>
      <div className="flex items-center gap-3 text-[11px] text-slate-500">
        <span>{location}</span>
      </div>
      <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-600">
        <span className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5">
          {project.subcontracts_count || 0} subcontracts
        </span>
        <span className="inline-flex items-center rounded-full bg-slate-100 px-2 py-0.5">
          {project.files_count || 0} files
        </span>
      </div>
    </button>
  )
}

export default ProjectCard

