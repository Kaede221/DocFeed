import axios from 'axios'
import type { FrameworkInfo, GenerateRequest, GenerateResponse } from '../types'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
})

export async function getFrameworks(): Promise<FrameworkInfo[]> {
  const { data } = await http.get<{ frameworks: FrameworkInfo[] }>('/frameworks')
  return data.frameworks
}

export async function generateContext(req: GenerateRequest): Promise<GenerateResponse> {
  const { data } = await http.post<GenerateResponse>('/generate', req)
  return data
}