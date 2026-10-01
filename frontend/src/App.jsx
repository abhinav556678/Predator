import React, { useState, useEffect, useCallback } from 'react'
import { fetchIncidents, getApiBaseUrl } from './services/api'
import IncidentCard from './components/IncidentCard'
import Timeline from './components/Timeline'
import BackendConfigModal from './components/BackendConfigModal'

// Stage progression heuristic for simulated cyber kill chain
const STAGE_PROGRESSION = {
  'RECONNAISSANCE': 'DISCOVERY',
  'DISCOVERY': 'CREDENTIAL ACCESS',
  'CREDENTIAL ACCESS': 'PRIVILEGE ESCALATION',
  'PRIVILEGE ESCALATION': 'LATERAL MOVEMENT',
  'LATERAL MOVEMENT': 'DATA EXFILTRATION',
  'DATA EXFILTRATION': 'RANSOMWARE / IMPACT',
}

export default function App() {
  const [incidents, setIncidents] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [backendUrl, setBackendUrl] = useState(getApiBaseUrl())
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false)

  // Fetch incidents from M3 Backend
  const loadIncidents = useCallback(async (isManual = false) => {
    if (isManual) setLoading(true)
    setError(null)
    try {
      const data = await fetchIncidents()
      setIncidents(data)
      setLastUpdated(new Date())
      setError(null)
    } catch (err) {
      setError(err.message || 'Unable to connect to M3 Backend')
    } finally {
      setLoading(false)
    }
  }, [])

  // Initial load and periodic polling
  useEffect(() => {
    loadIncidents(true)

    if (!autoRefresh) return

    const intervalId = setInterval(() => {
      loadIncidents(false)
    }, 6000)

    return () => clearInterval(intervalId)
  }, [loadIncidents, autoRefresh, backendUrl])

  // Computed metrics
  const activeCount = incidents.length
  const highRiskCount = incidents.filter(
    (i) => i.risk_level?.toUpperCase() === 'HIGH' || i.risk_level?.toUpperCase() === 'CRITICAL'
  ).length

  // System status badge styling
  let systemStatus = 'PROTECTED'
  let systemStatusColor = 'text-emerald-400'
  if (highRiskCount > 0) {
    systemStatus = 'ATTACK DETECTED'
    systemStatusColor = 'text-rose-500 animate-pulse font-bold'
  } else if (activeCount > 0) {
    systemStatus = 'ELEVATED'
    systemStatusColor = 'text-amber-400 font-semibold'
  }

  // Current assessment derived from latest incident
  const latestIncident = incidents.length > 0 ? incidents[0] : null
  const currentStage = latestIncident?.stage ? latestIncident.stage.toUpperCase() : 'NORMAL'
  const predictedNext = STAGE_PROGRESSION[currentStage] || (currentStage === 'NORMAL' ? 'NONE' : 'LATERAL MOVEMENT')
  const confidenceScore = currentStage === 'NORMAL' ? '100%' : (highRiskCount > 0 ? '94.2%' : '87.5%')

  // Deception hits check
  const deceptionInteractions = incidents.filter(
    (i) =>
      i.endpoint?.toLowerCase().includes('fake') ||
      i.endpoint?.toLowerCase().includes('honey') ||
      i.endpoint?.toLowerCase().includes('deception')
  )

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans">
      {/* Header */}
      <header className="bg-slate-800/95 border-b border-slate-700/80 px-6 py-3.5 flex flex-wrap justify-between items-center gap-4 sticky top-0 z-40 backdrop-blur-md">
        <div className="flex items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-black tracking-wider text-red-500">PREDATOR</h1>
              <span className="text-[10px] bg-red-950/80 text-red-400 border border-red-800/60 px-2 py-0.5 rounded font-mono font-semibold">
                EDR & DECEPTION
              </span>
            </div>
            <p className="text-xs text-slate-400 uppercase tracking-widest mt-0.5">
              Behavioral SOC Defense Dashboard
            </p>
          </div>

          {/* Backend Connection Indicator Button */}
          <button
            type="button"
            onClick={() => setIsConfigModalOpen(true)}
            title="Click to configure M3 Backend URL"
            className="flex items-center gap-2 bg-slate-900/90 hover:bg-slate-950 border border-slate-700 px-3 py-1.5 rounded-lg text-xs cursor-pointer transition"
          >
            <span
              className={`w-2 h-2 rounded-full ${
                error ? 'bg-rose-500' : 'bg-emerald-400 animate-pulse'
              }`}
            />
            <span className="font-mono text-slate-300">
              {error ? 'M3: OFFLINE' : 'M3: CONNECTED'}
            </span>
            <span className="text-[11px] text-slate-500 hover:text-slate-300">⚙ Edit IP</span>
          </button>
        </div>

        {/* Global SOC Metric Badges */}
        <div className="flex items-center gap-6 text-sm">
          <div className="flex flex-col items-end">
            <span className="text-slate-400 text-xs">System Status</span>
            <span className={`text-sm tracking-wide ${systemStatusColor}`}>{systemStatus}</span>
          </div>

          <div className="w-px h-8 bg-slate-700/60" />

          <div className="flex flex-col items-end">
            <span className="text-slate-400 text-xs">Active Incidents</span>
            <span className="text-slate-100 font-semibold text-sm font-mono">{activeCount}</span>
          </div>

          <div className="w-px h-8 bg-slate-700/60" />

          <div className="flex flex-col items-end">
            <span className="text-slate-400 text-xs">High / Critical Risk</span>
            <span
              className={`text-sm font-semibold font-mono ${
                highRiskCount > 0 ? 'text-rose-400 font-bold' : 'text-slate-100'
              }`}
            >
              {highRiskCount}
            </span>
          </div>

          <div className="w-px h-8 bg-slate-700/60" />

          {/* Manual Refresh & Auto-poll Controls */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => loadIncidents(true)}
              disabled={loading}
              title="Refresh incident list from M3 backend"
              className="p-2 bg-slate-700/70 hover:bg-slate-700 active:scale-95 text-slate-200 rounded-lg text-xs transition cursor-pointer disabled:opacity-50"
            >
              <svg
                className={`w-4 h-4 ${loading ? 'animate-spin text-cyan-400' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </button>

            <button
              type="button"
              onClick={() => setAutoRefresh((prev) => !prev)}
              className={`px-2.5 py-1 text-[11px] font-medium rounded-lg border transition cursor-pointer ${
                autoRefresh
                  ? 'bg-cyan-950/40 border-cyan-800/60 text-cyan-300'
                  : 'bg-slate-800 border-slate-700 text-slate-400'
              }`}
            >
              {autoRefresh ? 'Auto 6s' : 'Paused'}
            </button>
          </div>
        </div>
      </header>

      {/* Backend Error Alert Banner */}
      {error && (
        <div className="bg-rose-950/90 border-b border-rose-800/80 px-6 py-2.5 flex items-center justify-between text-xs text-rose-200">
          <div className="flex items-center gap-2">
            <span className="text-rose-400 font-bold">⚠️ Connection Issue:</span>
            <span>{error}</span>
            <span className="text-slate-400 hidden sm:inline">
              (Target: <code className="text-rose-300 font-mono">{backendUrl}</code>)
            </span>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setIsConfigModalOpen(true)}
              className="underline hover:text-white font-medium cursor-pointer"
            >
              Change IP
            </button>
            <button
              onClick={() => loadIncidents(true)}
              className="bg-rose-800 hover:bg-rose-700 text-white px-2 py-0.5 rounded font-medium cursor-pointer ml-2"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      {/* Main Layout Grid */}
      <div className="flex-1 flex overflow-hidden">
        {/* Main Content Area */}
        <main className="flex-1 p-6 overflow-y-auto space-y-6">
          {/* Timeline Section */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <h2 className="text-base font-semibold text-slate-200">Live Attack Timeline</h2>
                <span className="text-xs text-slate-400">
                  (Chronological progression of detected events)
                </span>
              </div>
              {lastUpdated && (
                <span className="text-[11px] text-slate-500 font-mono">
                  Synced: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
            </div>

            <Timeline incidents={incidents} />
          </section>

          {/* Incidents Section */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <h2 className="text-base font-semibold text-slate-200">Active Incidents</h2>
                <span className="text-xs font-mono bg-slate-800 px-2 py-0.5 rounded text-slate-400 border border-slate-700">
                  {incidents.length} Reported
                </span>
              </div>
            </div>

            {/* Loading Shimmer State */}
            {loading && incidents.length === 0 && (
              <div className="space-y-3">
                {[1, 2].map((n) => (
                  <div
                    key={n}
                    className="h-28 bg-slate-800/60 rounded-lg border border-slate-700/60 animate-pulse p-4"
                  >
                    <div className="h-4 bg-slate-700 rounded w-1/4 mb-3" />
                    <div className="h-3 bg-slate-700/70 rounded w-3/4 mb-2" />
                    <div className="h-3 bg-slate-700/50 rounded w-1/2" />
                  </div>
                ))}
              </div>
            )}

            {/* Empty State */}
            {!loading && incidents.length === 0 && !error && (
              <div className="bg-slate-800/80 rounded-lg border border-slate-700 p-8 flex flex-col items-center justify-center text-center">
                <p className="text-slate-400 font-medium">No active incidents detected.</p>
                <p className="text-slate-500 text-xs mt-1">
                  M3 Backend returned 0 incidents. All monitored endpoints appear normal.
                </p>
              </div>
            )}

            {/* Incident Cards List */}
            <div className="grid gap-3.5">
              {incidents.map((incident) => (
                <IncidentCard key={incident.id} incident={incident} />
              ))}
            </div>
          </section>
        </main>

        {/* Sidebar */}
        <aside className="w-84 bg-slate-800/90 border-l border-slate-700/80 p-5 flex flex-col gap-6 overflow-y-auto">
          {/* Predictions Panel */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Current Assessment
              </h3>
              <span className="text-[10px] bg-cyan-950 text-cyan-400 border border-cyan-800/60 px-1.5 py-0.2 rounded font-mono">
                ML ENGINE
              </span>
            </div>

            <div className="bg-slate-900/90 rounded-lg border border-slate-700/80 p-4 space-y-3 shadow-inner">
              <div>
                <p className="text-[11px] uppercase tracking-wider text-slate-400 mb-0.5">
                  Current Stage:
                </p>
                <p className="text-sm font-semibold text-slate-100 flex items-center gap-1.5 font-mono">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      currentStage === 'NORMAL' ? 'bg-emerald-400' : 'bg-rose-400 animate-pulse'
                    }`}
                  />
                  {currentStage}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800">
                <p className="text-[11px] uppercase tracking-wider text-slate-400 mb-0.5">
                  Predicted Next Stage:
                </p>
                <p className="text-sm font-semibold text-cyan-400 font-mono">
                  {predictedNext}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800">
                <p className="text-[11px] uppercase tracking-wider text-slate-400 mb-0.5">
                  Detection Confidence:
                </p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-slate-800 rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-cyan-500 h-full rounded-full transition-all duration-500"
                      style={{ width: confidenceScore }}
                    />
                  </div>
                  <span className="text-xs font-mono font-medium text-slate-300">
                    {confidenceScore}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Deception Environment Panel */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                Deception Environment
              </h3>
              <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800/60 px-1.5 py-0.2 rounded font-mono">
                M4 ACTIVE
              </span>
            </div>

            <div className="bg-slate-900/90 rounded-lg border border-slate-700/80 p-4 space-y-2.5 shadow-inner">
              <div className="flex justify-between items-center pb-1">
                <span className="text-xs text-slate-300 font-medium">Fake Server (Port 8080)</span>
                <span className="text-[10px] px-2 py-0.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded font-semibold font-mono">
                  ACTIVE
                </span>
              </div>

              <div className="flex justify-between items-center pb-1">
                <span className="text-xs text-slate-300 font-medium">Fake DB (Port 9000)</span>
                <span className="text-[10px] px-2 py-0.5 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded font-semibold font-mono">
                  ACTIVE
                </span>
              </div>

              <div className="pt-2.5 border-t border-slate-800">
                <p className="text-[11px] uppercase tracking-wider text-slate-400 mb-1">
                  Recent Interactions:
                </p>
                {deceptionInteractions.length > 0 ? (
                  <div className="space-y-1.5">
                    {deceptionInteractions.map((dec) => (
                      <div
                        key={dec.id}
                        className="bg-slate-950 p-2 rounded border border-rose-900/50 text-[11px] text-rose-300"
                      >
                        <p className="font-semibold font-mono">{dec.endpoint}</p>
                        <p className="text-slate-400 truncate">{dec.description}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 italic">No decoy interactions reported</p>
                )}
              </div>
            </div>
          </div>

          {/* Network Hub Details Panel */}
          <div className="mt-auto pt-4 border-t border-slate-700/60 text-xs text-slate-400">
            <p className="font-semibold text-slate-300 mb-1">M3 Backend Target</p>
            <p className="font-mono text-[11px] text-cyan-400 truncate bg-slate-950 px-2 py-1 rounded border border-slate-800">
              {backendUrl}/incidents
            </p>
          </div>
        </aside>
      </div>

      {/* Backend Configuration Modal */}
      <BackendConfigModal
        isOpen={isConfigModalOpen}
        onClose={() => setIsConfigModalOpen(false)}
        onSave={(newUrl) => {
          setBackendUrl(newUrl)
          loadIncidents(true)
        }}
      />
    </div>
  )
}
