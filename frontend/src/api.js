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

  // v3.1 Reviewer Experience
  reviewerPath: () => call('/demo/reviewer-path'),
  sampleOutputs: () => call('/demo/sample-outputs'),
  sampleOutput: (id) => call(`/demo/sample-output/${encodeURIComponent(id)}`),
  portfolioSummary: () => call('/demo/portfolio-summary'),

  // v3.2 Diagnostics
  diagnosticsHealth: () => call('/diagnostics/health'),
  diagnosticsIntegrity: () => call('/diagnostics/integrity'),
  diagnosticsSchemas: () => call('/diagnostics/schema-validation'),
  diagnosticsProject: () => call('/diagnostics/project-status'),

  // v4.0 Reasoning
  reasoningRuleMatch: (query) => call('/reasoning/rule-match', { method: 'POST', body: JSON.stringify({ query }) }),
  reasoningDecisionPath: (query) => call('/reasoning/decision-path', { method: 'POST', body: JSON.stringify({ query }) }),
  reasoningRiskScore: (query) => call('/reasoning/risk-score', { method: 'POST', body: JSON.stringify({ query }) }),
  reasoningEvidenceChain: (query) => call('/reasoning/evidence-chain', { method: 'POST', body: JSON.stringify({ query }) }),
  reasoningReasonedAnswer: (query) => call('/reasoning/reasoned-answer', { method: 'POST', body: JSON.stringify({ query }) }),
  reasoningPolicyExplanation: (query) => call('/reasoning/policy-explanation', { method: 'POST', body: JSON.stringify({ query }) }),

  // v4.5 Hybrid Retrieval
  hybridSearch: (body) => call('/retrieval/hybrid-search', { method: 'POST', body: JSON.stringify(body) }),
  retrievalCompare: (query) => call('/retrieval/compare', { method: 'POST', body: JSON.stringify({ query }) }),
  groundingReport: (answer, query) => call('/retrieval/grounding-report', { method: 'POST', body: JSON.stringify({ answer, query }) }),
  retrievalEvaluation: () => call('/retrieval/evaluation'),
  retrievalConflicts: () => call('/retrieval/conflicts'),
  retrievalSourceTrust: () => call('/retrieval/source-trust'),

  // v5.0 Agent Hub
  agentHubStatus: () => call('/agent-hub/status'),
  agentHubContext: (query) => call('/agent-hub/context', { method: 'POST', body: JSON.stringify({ query }) }),
  agentHubOrchestrate: (query) => call('/agent-hub/orchestrate', { method: 'POST', body: JSON.stringify({ query }) }),
  agentHubSkillEvidence: () => call('/agent-hub/skill-evidence'),
  agentHubMissingEvidence: () => call('/agent-hub/missing-evidence'),
  agentHubPortfolioReadiness: () => call('/agent-hub/portfolio-readiness'),
  agentHubCrossProjectReport: () => call('/agent-hub/cross-project-report'),
  agentHubMaturity: () => call('/agent-hub/maturity'),
  agentHubNextActions: () => call('/agent-hub/next-actions'),
  agentHubV5Release: () => call('/agent-hub/v5-release-report'),
}
