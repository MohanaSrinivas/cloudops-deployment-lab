const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
export async function request(path: string, token: string, init: RequestInit = {}) {
  const response = await fetch(`${API}${path}`, { ...init, headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}`, ...init.headers } });
  if (!response.ok) throw new Error((await response.json()).detail ?? `HTTP ${response.status}`);
  return response.status === 204 ? null : response.json();
}
