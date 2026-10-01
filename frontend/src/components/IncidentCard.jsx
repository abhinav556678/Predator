import React, { useState } from 'react'

/**
 * Returns Tailwind color classes tailored to incident risk levels.
 */
function getRiskStyle(level = '') {
  switch (level.toUpperCase()) {
    case 'CRITICAL':
      return {
        badge: 'bg-red-500/20 text-red-400 border-red-500/40',
        dot: 'bg-red-400 animate-pulse',
        border: 'border-l-red-500',
        glow: 'hover:shadow-red-500/10',
      }
    case 'HIGH':
      return {
        badge: 'bg-rose-500/20 text-rose-400 border-rose-500/40',
        dot: 'bg-rose-400 animate-pulse',
        border: 'border-l-rose-500',
        glow: 'hover:shadow-rose-500/10',
      }
    case 'MEDIUM':
      return {
        badge: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
        dot: 'bg-amber-400',
        border: 'border-l-amber-500',
        glow: 'hover:shadow-amber-500/10',
      }
    case 'LOW':
    default:
      return {
        badge: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
        dot: 'bg-emerald-400',
        border: 'border-l-emerald-500',
        glow: 'hover:shadow-emerald-500/10',
      }
  }
}

/**
 * Formats ISO timestamp to human-friendly local time and relative representation.
 */
function formatIncidentTime(isoString) {
  if (!isoString) return { formatted: 'Unknown', relative: '' }
  try {
    const date = new Date(isoString)
    const formatted = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    const fullDate = date.toLocaleDateString([], { month: 'short', day: 'numeric' })
    
    // Relative calculation
    const diffSec = Math.floor((Date.now() - date.getTime()) / 1000)
    let relative = 'Just now'
    if (diffSec >= 60 && diffSec < 3600) {
      relative = `${Math.floor(diffSec / 60)}m ago`
    } else if (diffSec >= 3600 && diffSec < 86400) {
      relative = `${Math.floor(diffSec / 3600)}h ago`
    } else if (diffSec >= 86400) {
      relative = `${Math.floor(diffSec / 86400)}d ago`
    }
    
    return { formatted: `${fullDate} ${formatted}`, relative }
  } catch {
    return { formatted: isoString, relative: '' }
  }
}

export default function IncidentCard({ incident }) {
  const [showDetails, setShowDetails] = useState(false)

  if (!incident) return null

  const { id, timestamp, stage, risk_level, endpoint, description } = incident
  const risk = getRiskStyle(risk_level)
  const time = formatIncidentTime(timestamp)

  return (
    <article
      className={`bg-slate-800/90 hover:bg-slate-800 transition-all duration-200 rounded-lg border border-slate-700/80 border-l-4 ${risk.border} p-4 shadow-md ${risk.glow}`}
    >
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2.5">
        <div className="flex items-center gap-2.5">
          <span className="font-mono text-xs font-semibold text-slate-200 bg-slate-900/90 px-2 py-0.5 rounded border border-slate-700">
            {id || 'INC-UNKNOWN'}
          </span>
          <span
            className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-0.5 rounded-full border ${risk.badge}`}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${risk.dot}`} />
            {risk_level || 'UNKNOWN'}
          </span>
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400 bg-slate-700/50 px-2 py-0.5 rounded">
            {stage || 'GENERAL'}
          </span>
        </div>

        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span title={timestamp} className="font-mono">
            {time.formatted} {time.relative && `(${time.relative})`}
          </span>
        </div>
      </div>

      {/* Incident Description */}
      <p className="text-sm text-slate-200 mb-3 leading-relaxed font-normal">
        {description || 'No description provided.'}
      </p>

      {/* Footer Info & Action */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-700/50 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Target Endpoint:</span>
          <code className="font-mono font-semibold text-cyan-400 bg-slate-900/80 px-2 py-0.5 rounded border border-slate-700/60">
            {endpoint || 'ALL-SYSTEMS'}
          </code>
        </div>

        <button
          type="button"
          onClick={() => setShowDetails((prev) => !prev)}
          className="text-xs text-slate-400 hover:text-slate-200 font-medium transition-colors cursor-pointer flex items-center gap-1"
        >
          {showDetails ? 'Hide JSON' : 'View Raw JSON'}
          <span className="text-xs">{showDetails ? '▲' : '▼'}</span>
        </button>
      </div>

      {/* Expandable JSON details */}
      {showDetails && (
        <div className="mt-3 pt-3 border-t border-slate-700/60">
          <pre className="text-[11px] font-mono bg-slate-950 text-emerald-400 p-3 rounded overflow-x-auto border border-slate-800">
            {JSON.stringify(incident, null, 2)}
          </pre>
        </div>
      )}
    </article>
  )
}
