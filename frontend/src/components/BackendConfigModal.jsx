import React, { useState } from 'react'
import { getApiBaseUrl, setApiBaseUrl, resetApiBaseUrl, checkBackendHealth } from '../services/api'

export default function BackendConfigModal({ isOpen, onClose, onSave }) {
  const [url, setUrl] = useState(getApiBaseUrl())
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState(null)

  if (!isOpen) return null

  const handleTest = async () => {
    setTesting(true)
    setTestResult(null)
    const original = getApiBaseUrl()
    // Temporarily set to test target
    setApiBaseUrl(url)
    const res = await checkBackendHealth()
    setTestResult(res)
    setTesting(false)
    if (!res.ok) {
      setApiBaseUrl(original) // revert if test failed
    }
  }

  const handleSave = () => {
    setApiBaseUrl(url)
    onSave(url)
    onClose()
  }

  const handleReset = () => {
    resetApiBaseUrl()
    const def = getApiBaseUrl()
    setUrl(def)
    setTestResult(null)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4">
      <div className="bg-slate-900 border border-slate-700 rounded-xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400" />
            M3 Backend Hub Configuration
          </h3>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-200 text-lg leading-none cursor-pointer"
          >
            ✕
          </button>
        </div>

        <p className="text-xs text-slate-400 mb-4 leading-relaxed">
          Configure the network address of Member 3's FastAPI backend hub. For local testing use{' '}
          <code className="text-cyan-400">http://127.0.0.1:8000</code> or enter M3's LAN IP (e.g.{' '}
          <code className="text-cyan-400">http://192.168.1.X:8000</code>).
        </p>

        <div className="mb-4">
          <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
            Backend API Base URL
          </label>
          <input
            type="text"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value)
              setTestResult(null)
            }}
            placeholder="http://127.0.0.1:8000"
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 font-mono focus:outline-none focus:border-cyan-500"
          />
        </div>

        {testResult && (
          <div
            className={`p-3 rounded-lg text-xs mb-4 border ${
              testResult.ok
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                : 'bg-red-500/10 border-red-500/30 text-red-300'
            }`}
          >
            {testResult.ok ? (
              <span>✓ Successfully connected to M3 backend ({testResult.latencyMs}ms latency)</span>
            ) : (
              <span>✗ Connection failed: {testResult.message}</span>
            )}
          </div>
        )}

        <div className="flex items-center justify-between gap-2 pt-2 border-t border-slate-800">
          <div className="flex gap-2">
            <button
              type="button"
              onClick={handleTest}
              disabled={testing}
              className="px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition cursor-pointer disabled:opacity-50"
            >
              {testing ? 'Testing...' : 'Test Connection'}
            </button>
            <button
              type="button"
              onClick={handleReset}
              className="px-2.5 py-1.5 text-xs text-slate-400 hover:text-slate-200 transition cursor-pointer"
            >
              Reset Default
            </button>
          </div>

          <div className="flex gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 text-xs rounded-lg text-slate-400 hover:text-slate-200 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSave}
              className="px-4 py-1.5 text-xs font-semibold rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white transition cursor-pointer shadow"
            >
              Save & Apply
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
