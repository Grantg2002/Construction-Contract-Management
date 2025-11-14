import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ProjectDetail from './pages/ProjectDetail'
import UploadProposal from './pages/UploadProposal'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50">
        <main className="overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/project/:id" element={<ProjectDetail />} />
            <Route path="/upload-proposal" element={<UploadProposal />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

