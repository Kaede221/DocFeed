export interface DocModule {
  name: string
  path: string
  label: string
}

export interface FrameworkInfo {
  id: string
  name: string
  repo: string
  docs_root: string
  modules: DocModule[]
}

export interface GenerateRequest {
  framework_id: string
  module_paths: string[]
}

export interface GenerateResponse {
  framework: string
  modules: string[]
  context: string
  file_count: number
  char_count: number
}