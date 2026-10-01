import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 p-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold tracking-wider text-red-500">PREDATOR</h1>
          <p className="text-xs text-slate-400 uppercase tracking-widest mt-1">SOC Dashboard</p>
        </div>
        <div className="flex gap-6 text-sm">
          <div className="flex flex-col items-end">
            <span className="text-slate-400">System Status</span>
            <span className="text-emerald-400 font-medium">PROTECTED</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-slate-400">Active Incidents</span>
            <span className="text-slate-100 font-medium">0</span>
          </div>
          <div className="flex flex-col items-end">
            <span className="text-slate-400">High Risk</span>
            <span className="text-slate-100 font-medium">0</span>
          </div>
        </div>
      </header>

      {/* Main Layout */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Main Content Area */}
        <main className="flex-1 p-6 overflow-y-auto">
          <h2 className="text-lg font-semibold mb-4 text-slate-300">Live Attack Timeline</h2>
          <div className="bg-slate-800 rounded border border-slate-700 p-4 mb-6 min-h-[200px] flex items-center justify-center">
            <p className="text-slate-500 italic">No events detected.</p>
          </div>

          <h2 className="text-lg font-semibold mb-4 text-slate-300">Active Incidents</h2>
          <div className="grid gap-4">
            {/* Placeholder for Incident Cards */}
            <div className="bg-slate-800 rounded border border-slate-700 p-4 flex items-center justify-center h-32">
              <p className="text-slate-500 italic">No active incidents.</p>
            </div>
          </div>
        </main>

        {/* Sidebar */}
        <aside className="w-80 bg-slate-800 border-l border-slate-700 p-6 flex flex-col gap-6 overflow-y-auto">
          {/* Predictions Panel */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">Current Assessment</h3>
            <div className="bg-slate-900 rounded border border-slate-700 p-4">
              <div className="mb-3">
                <p className="text-xs text-slate-400 mb-1">Current Stage:</p>
                <p className="text-sm font-medium text-slate-200">NORMAL</p>
              </div>
              <div className="mb-3">
                <p className="text-xs text-slate-400 mb-1">Predicted Next:</p>
                <p className="text-sm font-medium text-slate-200">NONE</p>
              </div>
              <div>
                <p className="text-xs text-slate-400 mb-1">Confidence:</p>
                <p className="text-sm font-medium text-slate-200">100%</p>
              </div>
            </div>
          </div>

          {/* Deception Panel */}
          <div>
            <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-3">Deception Environment</h3>
            <div className="bg-slate-900 rounded border border-slate-700 p-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-slate-300">Fake Server</span>
                <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded">ACTIVE</span>
              </div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-slate-300">Fake DB</span>
                <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded">ACTIVE</span>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-800">
                <p className="text-xs text-slate-400 mb-1">Recent Interactions:</p>
                <p className="text-sm text-slate-500 italic">None</p>
              </div>
            </div>
          </div>
        </aside>

      </div>
    </div>
  )
}

export default App
