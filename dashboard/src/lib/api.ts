import { isAuthenticated } from '../stores/auth';

const BASE_URL = import.meta.env.VITE_API_URL || 'https://rout3-backend.vercel.app/api/v1';

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('authToken');
  const headers: HeadersInit = {
    ...options.headers,
  };

  if (!(headers as any)['Content-Type'] && !options.body?.toString().includes('FormData')) {
     (headers as any)['Content-Type'] = 'application/json';
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      isAuthenticated.set(false);
      localStorage.removeItem('authToken');
    }
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

export const api = {
  get: <T>(endpoint: string) => request<T>(endpoint, { method: 'GET' }),
  post: <T>(endpoint: string, body: any) => request<T>(endpoint, { method: 'POST', body: JSON.stringify(body) }),
  postForm: <T>(endpoint: string, body: URLSearchParams) => request<T>(endpoint, { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body 
  }),
  put: <T>(endpoint: string, body: any) => request<T>(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
  delete: <T>(endpoint: string) => request<T>(endpoint, { method: 'DELETE' }),
};
