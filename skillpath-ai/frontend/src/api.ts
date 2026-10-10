import type { Analysis, Profile } from './types'

const API_BASE = import.meta.env.VITE_API_BASE_URL || (typeof window !== 'undefined' && window.location.port === '5173' ? 'http://127.0.0.1:8000' : '')

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response
  try { response = await fetch(`${API_BASE}${path}`, init) }
  catch { throw new Error('Cannot reach the backend. Start FastAPI at http://127.0.0.1:8000 and try again.') }
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`)
  return body as T
}
export const api = {
  careers: () => request<{id:string;name:string}[]>('/api/careers'),
  saveProfile: (profile: Profile) => request('/api/profile', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(profile)}),
  analyze: (profile: Profile) => request<Analysis>('/api/career/analyze', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({profile, target_career:profile.target_career})}),
  analyzeResume: (text: string) => {
    const form = new FormData(); form.append('text', text)
    return request<{skills:string[];education:Record<string,string>;projects:string[];experience:string[];certifications:string[];confidence:number;method:string}>('/api/resume/analyze', {method:'POST', body:form})
  },
  analyzeResumeFile: (file: File) => {
    const form = new FormData(); form.append('file', file)
    return request<{skills:string[];education:Record<string,string>;projects:string[];experience:string[];certifications:string[];confidence:number;method:string}>('/api/resume/analyze', {method:'POST', body:form})
  },
}
