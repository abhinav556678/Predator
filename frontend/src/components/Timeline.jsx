import React from 'react'

/**
 * Stage order helper for visual timeline representation
 */
function getStageColor(riskLevel = '') {
  switch (riskLevel.toUpperCase()) {
    case 'CRITICAL':
      return { dot: 'bg-red-500 ring-4 ring-red-500/20', line: 'border-red-500/40' }
    case 'HIGH':
      return { dot: 'bg-rose-500 ring-4 ring-rose-500/20', line: 'border-rose-500/40' }
    case 'MEDIUM':
      return { dot: 'bg-amber-400 ring-4 ring-amber-400/20', line: 'border-amber-400/40' }
    case 'LOW':
    default:
      return { dot: 'bg-emerald-400 ring-4 ring-emerald-400/20', line: 'border-emerald-400/40' }
  }
}

function formatTimelineTime(isoString) {
  if (!isoString) return '--:--:--'
  try {
    const d = new Date(isoString)
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  } catch {
    return isoString
  }
}

export default function Timeline({ incidents = [] }) {
  if (!incidents || incidents.length === 0) {
    return (
      <div className="bg-slate-800/80 rounded-lg border border-slate-700/80 p-8 flex flex-col items-center justify-center text-center">
        <div className="w-10 h-10 rounded-full bg-slate-700/50 flex items-center justify-center text-slate-400 mb-3">
          <svg className="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p className="text-slate-400 font-medium text-sm">No attack events detected</p>
        <p className="text-slate-500 text-xs mt-1">Timeline updates dynamically as incidents are reported by M3 backend</p>
      </div>
    )
  }

  // Display chronologically (earliest to latest or latest to earliest)
  const sorted = [...incidents].sort((a, b) => {
    const timeA = new Date(a.timestamp || 0).getTime()
    const timeB = new Date(b.timestamp || 0).getTime()
    return timeB - timeA // Latest on top
  })

  return (
    <div className="bg-slate-800/90 rounded-lg border border-slate-700/80 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-700/60">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          Chronological Event Sequence ({incidents.length} Events)
        </span>
        <span className="inline-flex items-center gap-1.5 text-xs text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          Live Sequence
        </span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-700">
        {sorted.map((item, index) => {
          const colors = getStageColor(item.risk_level)
          const isLatest = index === 0

          return (
            <div key={item.id || index} className="relative group">
              {/* Timeline Node Icon */}
              <div
                className={`absolute -left-[27px] top-1.5 w-3 h-3 rounded-full transition-transform group-hover:scale-125 ${colors.dot}`}
              />

              <div className="bg-slate-900/60 rounded-md border border-slate-700/60 p-3 hover:border-slate-600 transition-colors">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold uppercase tracking-wide text-slate-200">
                      {item.stage || 'STAGE UNKNOWN'}
                    </span>
                    {isLatest && (
                      <span className="text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/30 px-1.5 py-0.2 rounded uppercase">
                        Latest
                      </span>
                    )}
                  </div>
                  <span className="font-mono text-xs text-slate-400">
                    {formatTimelineTime(item.timestamp)}
                  </span>
                </div>

                <p className="text-xs text-slate-300 mb-2 leading-relaxed">
                  {item.description}
                </p>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1 border-t border-slate-800/80">
                  <span className="font-mono">
                    ID: <strong className="text-slate-300 font-semibold">{item.id}</strong>
                  </span>
                  <span>
                    Endpoint: <strong className="text-cyan-400 font-mono">{item.endpoint}</strong>
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
