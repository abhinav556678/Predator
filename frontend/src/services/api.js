/**
 * API Service for PREDATOR Frontend
 * Connects React UI to M3 Backend Hub (http://<M3_IP>:8000)
 */

const STORAGE_KEY_API_URL = 'predator_m3_api_url';
const DEFAULT_API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

/**
 * Returns the currently configured M3 Backend base URL.
 * Checks localStorage first for runtime overrides, then falls back to VITE_API_URL or localhost.
 */
export function getApiBaseUrl() {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem(STORAGE_KEY_API_URL);
    if (saved) return saved.replace(/\/+$/, '');
  }
  return DEFAULT_API_URL.replace(/\/+$/, '');
}

/**
 * Sets a custom M3 backend URL at runtime (e.g., http://192.168.1.105:8000)
 */
export function setApiBaseUrl(url) {
  if (typeof window !== 'undefined') {
    if (!url) {
      localStorage.removeItem(STORAGE_KEY_API_URL);
    } else {
      localStorage.setItem(STORAGE_KEY_API_URL, url.trim().replace(/\/+$/, ''));
    }
  }
}

/**
 * Returns the WebSocket URL for the M3 Backend.
 */
export function getWebSocketUrl() {
  const baseUrl = getApiBaseUrl();
  // Convert http/https to ws/wss
  return baseUrl.replace(/^http/, 'ws') + '/ws/incidents';
}

/**
 * Resets the backend URL to the default build-time environment configuration.
 */
export function resetApiBaseUrl() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(STORAGE_KEY_API_URL);
  }
}

/**
 * Checks connectivity to the M3 Backend.
 * @returns {Promise<{ ok: boolean, latencyMs?: number, message?: string }>}
 */
export async function checkBackendHealth() {
  const baseUrl = getApiBaseUrl();
  const startTime = Date.now();
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 4000);

  try {
    const response = await fetch(`${baseUrl}/`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (response.ok) {
      return { ok: true, latencyMs: Date.now() - startTime };
    }
    return { ok: false, message: `Backend responded with HTTP ${response.status}` };
  } catch (err) {
    clearTimeout(timeoutId);
    return {
      ok: false,
      message: err.name === 'AbortError' ? 'Connection timed out' : (err.message || 'Network unreachable')
    };
  }
}

/**
 * Fetches the list of active incidents from M3 Backend (`/incidents`).
 * @param {object} [options]
 * @param {AbortSignal} [options.signal]
 * @returns {Promise<Array<{ id: string, timestamp: string, stage: string, risk_level: string, endpoint: string, description: string }>>}
 */
export async function fetchIncidents(options = {}) {
  const baseUrl = getApiBaseUrl();
  const controller = new AbortController();
  const timeoutMs = 8000;
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  const signal = options.signal
    ? AbortSignal.any
      ? AbortSignal.any([options.signal, controller.signal])
      : controller.signal
    : controller.signal;

  try {
    const response = await fetch(`${baseUrl}/incidents`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    if (!Array.isArray(data)) {
      throw new Error('Invalid response format: expected an array of incidents.');
    }

    return data;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      throw new Error(`Request timed out while connecting to M3 Backend at ${baseUrl}`);
    }
    throw new Error(`Failed to fetch incidents from ${baseUrl}: ${err.message}`);
  }
}
