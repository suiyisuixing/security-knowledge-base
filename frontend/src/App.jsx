import React, { useEffect, useState } from 'react'
import { api } from './api.js'

function Badge({ kind, children }) {
  return <span className={`badge ${kind}`}>{children}</span>
}

function classBadge(allowed, classification) {
  if (classification && classification.startsWith('blocked_')) return 'red'
  if (classification && classification.startsWith('needs_')) return 'yellow'
  if (allowed) return 'green'
  return 'gray'
}

function Card({ title, children, className }) {
  return (
    <section className={`card ${className || ''}`}>
      <h2>{title}</h2>
      {children}
    </section>
  )
}

function LocalOnlyBanner() {
  return (
    <div className="banner blue">
      This is a local-only, model-free, defensive, authorized-scope portfolio project.
      It does not use LLMs, perform real scanning, or execute exploitation.
      <br />
      <span className="muted">本项目本地、无大模型、防御性、授权范围内，不使用大模型、不执行真实扫描、不执行漏洞利用。</span>
    </div>
  )
}

function HealthCard() {
  const [data, setData] = useState(null)
  const [err, setErr] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    api.health().then(d => { setData(d); setLoading(false) }).catch(e => { setErr(String(e)); setLoading(false) })
  }, [])
  return (
    <Card title="Backend Status">
      {loading && <p className="muted">checking...</p>}
      {err && <p><Badge kind="red">offline</Badge> {err}</p>}
      {data && <p><Badge kind="green">online</Badge> version <span className="kbd">{data.version}</span></p>}
    </Card>
  )
}

function DisclosureCard() {
  return (
    <Card title="Development Note · AI-assisted Disclosure" className="disclosure">
      <p>
        This project was developed as an AI-assisted learning and engineering project.
        The architecture, security knowledge model, safety policy design, testing goals,
        validation process, and final review were directed by the author. AI tools were
        used for planning, documentation support, debugging guidance, and review
        assistance, while all repository commits and project decisions were managed by
        the author.
      </p>
    </Card>
  )
}

function PortfolioOverview() {
  const [projects, setProjects] = useState([])
  const [domains, setDomains] = useState(null)
  useEffect(() => {
    api.projects().then(d => setProjects(d.projects)).catch(()=>{})
    api.domains().then(setDomains).catch(()=>{})
  }, [])
  return (
    <Card title="Portfolio Knowledge Overview · A / B / C / D">
      <p>Knowledge layer connecting A/B/C/D projects.</p>
      <table>
        <thead><tr><th>Project</th><th>Focus</th><th>Skills</th></tr></thead>
        <tbody>
          {projects.map(p => (
            <tr key={p.project_id}>
              <td><strong>{p.name}</strong><div className="muted">{p.project_id}</div></td>
              <td>{p.focus}</td>
              <td>{(p.skills || []).map(s => <Badge key={s} kind="blue">{s}</Badge>)}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {domains && (
        <p className="muted">
          Domains: {domains.domains.join(', ')} ·
          Documents: {Object.values(domains.counts || {}).reduce((a,b)=>a+b, 0)}
        </p>
      )}
    </Card>
  )
}

function SearchPanel() {
  const [q, setQ] = useState('prompt injection')
  const [results, setResults] = useState([])
  const [err, setErr] = useState(null)
  const search = () => { setErr(null); api.search({ query: q, top_k: 5 }).then(d => setResults(d.results)).catch(e => setErr(String(e))) }
  return (
    <Card title="Knowledge Search">
      <input value={q} onChange={e => setQ(e.target.value)} placeholder="e.g. BOLA authorization" />
      <p><button onClick={search}>Search</button></p>
      {err && <p><Badge kind="red">error</Badge> {err}</p>}
      <table>
        <thead><tr><th>Doc</th><th>Domain</th><th>Score</th></tr></thead>
        <tbody>
          {results.map(r => (
            <tr key={r.doc_id}>
              <td>{r.title}<div className="muted">{r.doc_id}</div></td>
              <td><Badge kind="blue">{r.domain}</Badge></td>
              <td>{r.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  )
}

function AskPanel() {
  const [q, setQ] = useState('Explain what BOLA is.')
  const [answer, setAnswer] = useState(null)
  const ask = () => api.ask({ query: q, top_k: 5 }).then(setAnswer)
  return (
    <Card title="Knowledge-grounded Answer">
      <textarea value={q} onChange={e => setQ(e.target.value)} />
      <p><button onClick={ask}>Ask</button></p>
      {answer && (
        <>
          <pre>{answer.answer}</pre>
          <p>Citations: {(answer.citations || []).map(c => <Badge key={c.doc_id} kind="blue">{c.doc_id}</Badge>)}</p>
          <p className="muted">Safety: {answer.safety_note}</p>
        </>
      )}
    </Card>
  )
}

function SafetyPanel() {
  const [text, setText] = useState('Scan this public IP for vulnerabilities.')
  const [result, setResult] = useState(null)
  const go = () => api.classify(text).then(setResult)
  return (
    <Card title="Safety Policy Classifier">
      <textarea value={text} onChange={e => setText(e.target.value)} />
      <p><button onClick={go}>Classify</button></p>
      {result && (
        <>
          <p><Badge kind={classBadge(result.allowed, result.classification)}>{result.classification}</Badge>
            {' '}<Badge kind={result.allowed ? 'green' : 'red'}>{result.allowed ? 'allowed' : 'not allowed'}</Badge></p>
          <p className="muted">{result.reason}</p>
          <p className="muted">Safe redirect: {result.safe_redirect}</p>
        </>
      )}
    </Card>
  )
}

function MemoryPanel() {
  const [profile, setProfile] = useState(null)
  useEffect(() => { api.memory().then(setProfile).catch(()=>{}) }, [])
  if (!profile) return <Card title="Agent Memory"><p className="muted">loading...</p></Card>
  return (
    <Card title="Agent Memory">
      <p><strong>{profile.display_name}</strong></p>
      <p className="muted">Goals: {(profile.goals || []).join(' · ')}</p>
      <table>
        <thead><tr><th>Skill</th><th>Status</th></tr></thead>
        <tbody>
          {(profile.skill_progress || []).map(s => (
            <tr key={s.skill_id}>
              <td>{s.skill_id}</td>
              <td><Badge kind={s.status === 'in_progress' ? 'yellow' : s.status === 'completed' ? 'green' : 'gray'}>{s.status}</Badge></td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  )
}

function ProjectSkillMapper() {
  const [skills, setSkills] = useState([])
  useEffect(() => { api.skills().then(d => setSkills(d.skills)).catch(()=>{}) }, [])
  return (
    <Card title="Project / Skill Mapper">
      <table>
        <thead><tr><th>Skill</th><th>Domain</th><th>Projects</th></tr></thead>
        <tbody>
          {skills.map(s => (
            <tr key={s.skill_id}>
              <td>{s.name}<div className="muted">{s.skill_id}</div></td>
              <td><Badge kind="blue">{s.domain}</Badge></td>
              <td>{(s.related_projects || []).map(p => <Badge key={p} kind="gray">{p}</Badge>)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </Card>
  )
}

function LearningPathPanel() {
  const [goal, setGoal] = useState('Learn AI security fundamentals')
  const [path, setPath] = useState(null)
  const go = () => api.learningPath({ goal }).then(setPath)
  return (
    <Card title="Learning Path">
      <input value={goal} onChange={e => setGoal(e.target.value)} />
      <p><button onClick={go}>Generate</button></p>
      {path && (
        <ol className="path-steps">
          {path.steps.map(s => (
            <li key={s.step}><strong>{s.title}</strong> <span className="muted">— {s.notes}</span></li>
          ))}
        </ol>
      )}
    </Card>
  )
}

function AuthorizedWorkflowPanel() {
  const [text, setText] = useState('Plan limited authorized recon inside my bug bounty scope.')
  const [wf, setWf] = useState(null)
  const go = () => api.authorizedPlan({ request: text }).then(setWf)
  return (
    <Card title="Authorized Workflow Planner">
      <textarea value={text} onChange={e => setText(e.target.value)} />
      <p><button onClick={go}>Plan</button></p>
      {wf && (
        <>
          <p><Badge kind={wf.allowed ? 'green' : 'red'}>{wf.allowed ? 'allowed' : 'blocked'}</Badge> scope: <span className="kbd">{wf.required_scope}</span></p>
          <p className="muted">{wf.summary}</p>
          <p><strong>Steps</strong></p>
          <ol>{(wf.steps || []).map((s,i) => <li key={i}>{s}</li>)}</ol>
          <p><strong>Blocked actions</strong></p>
          <ul>{(wf.blocked_actions || []).map((s,i) => <li key={i}>{s}</li>)}</ul>
        </>
      )}
    </Card>
  )
}

function TaskRouterPanel() {
  const [q, setQ] = useState('Help me triage these SOC alerts.')
  const [route, setRoute] = useState(null)
  const go = () => api.routeTask(q).then(setRoute)
  return (
    <Card title="Task Router">
      <input value={q} onChange={e => setQ(e.target.value)} />
      <p><button onClick={go}>Route</button></p>
      {route && (
        <p>
          → project: <Badge kind="blue">{route.project_id}</Badge>
          {' '}domain: <Badge kind="blue">{route.knowledge_domain}</Badge>
          {' '}skill: <Badge kind="gray">{route.skill_id}</Badge>
        </p>
      )}
    </Card>
  )
}

function KnowledgeQualityPanel() {
  const [data, setData] = useState(null)
  const load = () => api.knowledgeQuality().then(setData)
  return (
    <Card title="Knowledge Quality">
      <button onClick={load}>Score documents</button>
      {data && <p className="muted">avg {data.summary.average} · min {data.summary.min} · max {data.summary.max} · count {data.summary.count}</p>}
    </Card>
  )
}

function BenchmarkDashboard() {
  const [data, setData] = useState(null)
  const run = () => api.benchmarkRun().then(setData)
  return (
    <Card title="Benchmark Dashboard">
      <p>Run the agent benchmark and view summary.</p>
      <button onClick={run}>Run benchmark</button>
      {data && (
        <>
          <p>
            <Badge kind="green">passed {data.summary.passed}</Badge>
            <Badge kind="gray">total {data.summary.total}</Badge>
            <Badge kind="blue">pass rate {data.summary.pass_rate}</Badge>
          </p>
          <pre>{JSON.stringify(data.summary.by_type, null, 2)}</pre>
        </>
      )}
    </Card>
  )
}

function ReportsPanel() {
  const [report, setReport] = useState(null)
  const load = (kind) => {
    const p =
      kind === 'kb' ? api.reportKnowledge() :
      kind === 'safety' ? api.reportSafety() :
      api.reportReadiness()
    p.then(setReport)
  }
  return (
    <Card title="Reports">
      <p>
        <button onClick={() => load('kb')}>Knowledge coverage</button>{' '}
        <button onClick={() => load('safety')} className="secondary">Safety policy</button>{' '}
        <button onClick={() => load('readiness')} className="secondary">Agent readiness</button>
      </p>
      {report && <pre>{report.markdown}</pre>}
    </Card>
  )
}

// ============================================================
// v3.1 Reviewer Mode
// ============================================================

function ReviewerModePanel() {
  const [path, setPath] = useState(null)
  const [samples, setSamples] = useState([])
  const [active, setActive] = useState(null)
  useEffect(() => {
    api.reviewerPath().then(setPath).catch(()=>{})
    api.sampleOutputs().then(d => setSamples(d.samples)).catch(()=>{})
  }, [])
  return (
    <Card title="Reviewer Mode · One-click Sample Demo" className="reviewer">
      {path && (
        <>
          <p className="muted">{path.title} — {path.steps.length} steps</p>
          <ol>{path.steps.map(s => <li key={s.step}><strong>{s.action}</strong> <code className="kbd">{s.endpoint}</code></li>)}</ol>
          <p className="muted">{path.safety_boundary}</p>
        </>
      )}
      <h3>Sample outputs</h3>
      <div className="chip-row">
        {samples.map(s => (
          <button key={s.sample_id} className="chip" onClick={() => api.sampleOutput(s.sample_id).then(setActive)}>
            {s.sample_id}
          </button>
        ))}
      </div>
      {active && <pre>{JSON.stringify(active, null, 2)}</pre>}
    </Card>
  )
}

function PortfolioValueCard() {
  const [data, setData] = useState(null)
  useEffect(() => { api.portfolioSummary().then(setData).catch(()=>{}) }, [])
  if (!data) return null
  return (
    <Card title="Portfolio Value Summary">
      <p className="muted">{data.tagline}</p>
      <ul>{(data.value || []).map((v,i) => <li key={i}>{v}</li>)}</ul>
      <div className="chip-row">
        {(data.portfolio_links || []).map(p => (
          <Badge key={p.project_id} kind="gray">{p.project_id} · {p.focus}</Badge>
        ))}
      </div>
    </Card>
  )
}

// ============================================================
// v3.2 Diagnostics
// ============================================================

function DiagnosticsPanel() {
  const [data, setData] = useState(null)
  const load = () => api.diagnosticsProject().then(setData)
  return (
    <Card title="Backend Diagnostics · Integrity · Schema">
      <button onClick={load}>Run diagnostics</button>
      {data && (
        <>
          <p>
            <Badge kind={data.integrity.ok ? 'green' : 'red'}>integrity {data.integrity.ok ? 'ok' : 'failed'}</Badge>
            <Badge kind={data.schema_validation.all_valid ? 'green' : 'red'}>schemas {data.schema_validation.all_valid ? 'valid' : 'invalid'}</Badge>
            <Badge kind="blue">model_free</Badge>
          </p>
          <pre>{JSON.stringify(data.health.backend, null, 2)}</pre>
        </>
      )}
    </Card>
  )
}

// ============================================================
// v4.0 Reasoning
// ============================================================

function ReasoningPanel() {
  const [q, setQ] = useState('Scan this public IP for vulnerabilities.')
  const [rules, setRules] = useState(null)
  const [path, setPath] = useState(null)
  const [risk, setRisk] = useState(null)
  return (
    <Card title="Rule-based Reasoning · Decision Path · Risk Score">
      <textarea value={q} onChange={e => setQ(e.target.value)} />
      <p>
        <button onClick={() => api.reasoningRuleMatch(q).then(setRules)}>Match rules</button>{' '}
        <button onClick={() => api.reasoningDecisionPath(q).then(setPath)} className="secondary">Decision path</button>{' '}
        <button onClick={() => api.reasoningRiskScore(q).then(setRisk)} className="secondary">Risk score</button>
      </p>
      {rules && <pre>{JSON.stringify(rules.top_rule, null, 2)}</pre>}
      {path && <p>decision: <Badge kind={path.allowed ? 'green' : 'red'}>{path.decision}</Badge> confidence: {path.confidence}</p>}
      {risk && <p>level: <Badge kind={risk.overall.level === 'blocked' ? 'red' : risk.overall.level === 'high' ? 'red' : risk.overall.level === 'medium' ? 'yellow' : 'green'}>{risk.overall.level}</Badge> score: {risk.overall.score}</p>}
    </Card>
  )
}

function EvidenceChainPanel() {
  const [q, setQ] = useState('Explain BOLA')
  const [data, setData] = useState(null)
  return (
    <Card title="Evidence Chain · Policy Explanation">
      <input value={q} onChange={e => setQ(e.target.value)} />
      <p>
        <button onClick={() => api.reasoningEvidenceChain(q).then(setData)}>Build evidence</button>{' '}
        <button onClick={() => api.reasoningReasonedAnswer(q).then(setData)} className="secondary">Reasoned answer</button>
      </p>
      {data && <pre>{JSON.stringify(data, null, 2).slice(0, 2400)}</pre>}
    </Card>
  )
}

// ============================================================
// v4.5 Hybrid Retrieval
// ============================================================

function HybridRetrievalPanel() {
  const [q, setQ] = useState('Explain BOLA')
  const [hybrid, setHybrid] = useState(null)
  const [cmp, setCmp] = useState(null)
  return (
    <Card title="Hybrid Retrieval · Legacy vs Hybrid">
      <input value={q} onChange={e => setQ(e.target.value)} />
      <p>
        <button onClick={() => api.hybridSearch({ query: q, top_k: 5 }).then(setHybrid)}>Hybrid search</button>{' '}
        <button onClick={() => api.retrievalCompare(q).then(setCmp)} className="secondary">Compare</button>
      </p>
      {hybrid && (
        <table>
          <thead><tr><th>Doc</th><th>Score</th><th>Components</th></tr></thead>
          <tbody>
            {(hybrid.results || []).map(r => (
              <tr key={r.chunk_id}>
                <td>{r.title}<div className="muted">{r.doc_id}</div></td>
                <td>{r.score}</td>
                <td>{JSON.stringify(r.components)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {cmp && (
        <p>
          <Badge kind="gray">legacy {cmp.legacy.length}</Badge>
          <Badge kind="blue">hybrid {cmp.hybrid.length}</Badge>
          <Badge kind="green">overlap {cmp.overlap_count}</Badge>
        </p>
      )}
    </Card>
  )
}

function SourceTrustPanel() {
  const [data, setData] = useState(null)
  const load = () => api.retrievalSourceTrust().then(setData)
  return (
    <Card title="Source Trust · Knowledge Conflict">
      <button onClick={load}>Score sources</button>
      {data && (
        <p className="muted">scored {data.count} sources. Sample top-5:</p>
      )}
      {data && (
        <table>
          <thead><tr><th>Doc</th><th>Trust</th><th>Safety</th></tr></thead>
          <tbody>
            {(data.items || []).slice(0, 5).map(it => (
              <tr key={it.doc_id}><td>{it.title}</td><td>{it.trust}</td><td>{it.safety}</td></tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  )
}

// ============================================================
// v5.0 Agent Hub
// ============================================================

function AgentHubDashboard() {
  const [status, setStatus] = useState(null)
  const [orch, setOrch] = useState(null)
  const [q, setQ] = useState('Explain BOLA')
  useEffect(() => { api.agentHubStatus().then(setStatus).catch(()=>{}) }, [])
  return (
    <Card title="v5.0 Agent Hub" className="hub">
      {status && (
        <p>
          <Badge kind="green">model_free</Badge>
          <Badge kind="green">fully_local</Badge>
          <Badge kind="blue">projects tracked {status.projects_tracked}</Badge>
          <Badge kind="gray">version {status.version}</Badge>
        </p>
      )}
      <input value={q} onChange={e => setQ(e.target.value)} />
      <p><button onClick={() => api.agentHubOrchestrate(q).then(setOrch)}>Orchestrate</button></p>
      {orch && (
        <>
          <p>mode: <Badge kind="blue">{orch.mode}</Badge> route: <Badge kind="gray">{orch.route.project_id}</Badge></p>
          <pre>{JSON.stringify(orch.classification, null, 2)}</pre>
        </>
      )}
    </Card>
  )
}

function SkillEvidenceTracker() {
  const [data, setData] = useState(null)
  const [missing, setMissing] = useState(null)
  useEffect(() => {
    api.agentHubSkillEvidence().then(setData).catch(()=>{})
    api.agentHubMissingEvidence().then(setMissing).catch(()=>{})
  }, [])
  return (
    <Card title="Skill Evidence Tracker">
      {data && <p className="muted">{data.count} skills with evidence</p>}
      {data && (
        <table>
          <thead><tr><th>Skill</th><th>Score</th></tr></thead>
          <tbody>
            {(data.items || []).slice(0, 10).map(it => (
              <tr key={it.skill_id}><td>{it.skill_id}</td><td>{it.score}</td></tr>
            ))}
          </tbody>
        </table>
      )}
      {missing && <p>Missing: {(missing.missing_skills || []).map(s => <Badge key={s} kind="yellow">{s}</Badge>)}</p>}
    </Card>
  )
}

function PortfolioReadinessPanel() {
  const [data, setData] = useState(null)
  const load = () => api.agentHubPortfolioReadiness().then(setData)
  return (
    <Card title="Portfolio Readiness · Maturity">
      <button onClick={load}>Compute readiness</button>
      {data && (
        <>
          <p>overall: <Badge kind="green">{data.overall}</Badge></p>
          <table>
            <thead><tr><th>Category</th><th>Score</th></tr></thead>
            <tbody>
              {Object.entries(data.categories || {}).map(([k,v]) => (
                <tr key={k}><td>{k}</td><td>{v}</td></tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </Card>
  )
}

function NextActionsPanel() {
  const [plan, setPlan] = useState(null)
  const load = () => api.agentHubNextActions().then(setPlan)
  return (
    <Card title="Next Action Planner">
      <button onClick={load}>Plan next 30 days</button>
      {plan && (
        <>
          <p className="muted">{plan.safety_boundary}</p>
          <ul>{(plan.items || []).slice(0, 10).map((it,i) => <li key={i}>{it.suggestion || JSON.stringify(it)}</li>)}</ul>
        </>
      )}
    </Card>
  )
}

function V5ReleaseReportPanel() {
  const [data, setData] = useState(null)
  const load = () => api.agentHubV5Release().then(setData)
  return (
    <Card title="v5.0 Release Report">
      <button onClick={load}>Build report</button>
      {data && <pre>{data.notes}</pre>}
    </Card>
  )
}

function ReviewerQuickPath() {
  const steps = [
    'Load knowledge domains.',
    'Search for a security concept.',
    'Ask a knowledge-grounded question.',
    'Classify an allowed request.',
    'Classify a needs-confirmation request.',
    'Classify a blocked request.',
    'Generate a learning path.',
    'Build an authorized workflow plan.',
    'Route a task to A/B/C/D.',
    'Run benchmark.',
    'Generate agent readiness report.',
    'Review portfolio value summary.',
  ]
  return (
    <Card title="Reviewer Quick Path">
      <ol>{steps.map((s,i) => <li key={i}>{s}</li>)}</ol>
    </Card>
  )
}

export default function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>Security Knowledge Base &amp; Agent Memory Lab · v5.0-rc</h1>
        <p>Local cybersecurity knowledge base + rule-based reasoning + hybrid retrieval + agent hub for the A/B/C/D portfolio.</p>
      </header>
      <LocalOnlyBanner />
      <HealthCard />
      <DisclosureCard />
      <PortfolioValueCard />
      <PortfolioOverview />
      <div className="row">
        <div><SearchPanel /></div>
        <div><AskPanel /></div>
      </div>
      <div className="row">
        <div><SafetyPanel /></div>
        <div><MemoryPanel /></div>
      </div>
      <ProjectSkillMapper />
      <div className="row">
        <div><LearningPathPanel /></div>
        <div><AuthorizedWorkflowPanel /></div>
      </div>
      <div className="row">
        <div><TaskRouterPanel /></div>
        <div><KnowledgeQualityPanel /></div>
      </div>
      <BenchmarkDashboard />
      <ReportsPanel />
      <ReviewerModePanel />
      <DiagnosticsPanel />
      <div className="row">
        <div><ReasoningPanel /></div>
        <div><EvidenceChainPanel /></div>
      </div>
      <div className="row">
        <div><HybridRetrievalPanel /></div>
        <div><SourceTrustPanel /></div>
      </div>
      <AgentHubDashboard />
      <div className="row">
        <div><SkillEvidenceTracker /></div>
        <div><PortfolioReadinessPanel /></div>
      </div>
      <div className="row">
        <div><NextActionsPanel /></div>
        <div><V5ReleaseReportPanel /></div>
      </div>
      <ReviewerQuickPath />
      <p className="muted" style={{ textAlign: 'center', margin: '24px 0' }}>
        Local-only. No real targets. No real API keys. No real scanning. Model-free.
      </p>
    </div>
  )
}
