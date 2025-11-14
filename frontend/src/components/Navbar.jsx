function Navbar() {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-800">
          Construction Contract Management
        </h2>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">
            {new Date().toLocaleDateString()}
          </span>
        </div>
      </div>
    </header>
  )
}

export default Navbar

