const BASE = '/api-backend'

async function call(path, options = {}) {
  const res = await fetch(BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`${res.status}: ${text}`)
  }
  return res.json()
}

export const api = {
  health: () => call('/health'),
  domains: () => call('/knowledge/domains'),
  docs: (domain) => call('/knowledge/docs' + (domain ? `?domain=${encodeURIComponent(domain)}` : '')),
  getDoc: (id) => call(`/knowledge/docs/${encodeURIComponent(id)}`),
  search: (body) => call('/knowledge/search', { method: 'POST', body: JSON.stringify(body) }),
  ask: (body) => call('/knowledge/ask', { method: 'POST', body: JSON.stringify(body) }),
  classify: (text) => call('/safety/classify', { method: 'POST', body: JSON.stringify({ text }) }),
  safetyPolicy: () => call('/safety/policy'),
  safetyEval: () => call('/safety/evaluation'),
  memory: () => call('/memory/profile'),
  updateSkill: (body) => call('/memory/update-skill', { method: 'POST', body: JSON.stringify(body) }),
  audit: () => call('/memory/audit'),
  projects: () => call('/projects'),
  skills: () => call('/skills'),
  recommendSkills: (goal) => call('/skills/recommend', { method: 'POST', body: JSON.stringify({ goal }) }),
  learningPath: (body) => call('/learning-path/generate', { method: 'POST', body: JSON.stringify(body) }),
  context: (body) => call('/context/build', { method: 'POST', body: JSON.stringify(body) }),
  knowledgeQuality: () => call('/quality/knowledge'),
  reasoningTemplates: () => call('/reasoning/templates'),
  authorizedPlan: (body) => call('/workflow/authorized-plan', { method: 'POST', body: JSON.stringify(body) }),
  routeTask: (query) => call('/router/route-task', { method: 'POST', body: JSON.stringify({ query }) }),
  benchmarkTasks: () => call('/benchmark/tasks'),
  benchmarkRun: () => call('/benchmark/run', { method: 'POST' }),
  reportKnowledge: () => call('/report/knowledge-coverage', { method: 'POST' }),
  reportSafety: () => call('/report/safety-policy', { method: 'POST' }),
  reportReadiness: () => call('/report/agent-readiness', { method: 'POST' }),
  apiSurface: () => call('/api/surface'),
}
