// Retrieve API Key from Vite environment or development session
const API_KEY = (import.meta as any).env?.VITE_TRADEOS_API_KEY || 'tradeos_pilot_secret_key_2026';

export interface ApiFetchOptions extends RequestInit {
  skipAuth?: boolean;
}

export async function fetchApi<T>(endpoint: string, options: ApiFetchOptions = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (!options.skipAuth && API_KEY) {
    headers['X-TradeOS-Key'] = API_KEY;
  }

  const response = await fetch(endpoint, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.detail || `API error: ${response.statusText}`);
  }

  return response.json();
}
