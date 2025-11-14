function ProjectHeader({ project, onUploadProposalsClick, onFilesClick, onPermitsClick }) {
  // Format project start date
  const startDate = project.project_start_date 
    ? new Date(project.project_start_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
    : 'Not set'

  // Format location
  const location = project.city && project.state 
    ? `${project.city}, ${project.state}`
    : project.street || 'No location'

  return (
    <div className="pt-4 pb-5">
      {/* Background strip */}
      <div className="relative">
        <div className="h-10 rounded-2xl bg-slate-100 border border-slate-200" />
        
        {/* The "tab" */}
        <div className="absolute left-6 -top-3">
          <div className="inline-flex flex-col rounded-2xl bg-white border border-slate-200 px-4 py-2 shadow-sm">
            <div className="text-[11px] uppercase tracking-wide text-slate-400">
              Project
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-slate-900">
                {project.name}
              </span>
              <span className="text-[11px] text-slate-500">
                Start:{" "}
                <span className="font-medium text-slate-700">
                  {startDate}
                </span>
              </span>
            </div>
            <div className="flex items-center gap-3 mt-1 text-[11px] text-slate-500">
              <span>{location}</span>
              <span className="h-1 w-1 rounded-full bg-slate-300" />
              <span>{project.subcontracts_count || 0} subcontracts</span>
            </div>
          </div>
        </div>

        {/* Right side actions on the strip */}
        <div className="absolute right-4 top-1 flex items-center gap-2 text-[11px]">
          <button 
            onClick={onFilesClick}
            className="rounded-full border border-slate-200 px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-50"
          >
            Files
          </button>
          <button 
            onClick={onPermitsClick}
            className="rounded-full border border-slate-200 px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-50"
          >
            Permits
          </button>
          <button
            onClick={onUploadProposalsClick}
            className="rounded-full bg-slate-900 px-4 py-1.5 text-xs font-semibold text-white hover:bg-black"
          >
            Upload Proposals
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProjectHeader

