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

function HealthCard() {
  const [data, setData] = useState(null)
  const [err, setErr] = useState(null)
  useEffect(() => {
    api.health().then(setData).catch(e => setErr(String(e)))
  }, [])
  return (
    <Card title="Backend Status">
      {err && <p><Badge kind="red">offline</Badge> {err}</p>}
      {data && <p><Badge kind="green">online</Badge> version <span className="kbd">{data.version}</span></p>}
      {!data && !err && <p className="muted">checking...</p>}
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
    api.projects().then(d => setProjects(d.projects))
    api.domains().then(setDomains)
  }, [])
  return (
    <Card title="Portfolio Knowledge Overview">
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
  const search = () => api.search({ query: q, top_k: 5 }).then(d => setResults(d.results))
  return (
    <Card title="Knowledge Search">
      <input value={q} onChange={e => setQ(e.target.value)} placeholder="e.g. BOLA authorization" />
      <p><button onClick={search}>Search</button></p>
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
  useEffect(() => { api.memory().then(setProfile) }, [])
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
  useEffect(() => { api.skills().then(d => setSkills(d.skills)) }, [])
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

function ReviewerQuickPath() {
  const steps = [
    'Load knowledge domains.',
    'Search for a security concept.',
    'Ask a knowledge-grounded question.',
    'Classify a safety-sensitive request.',
    'Review project/skill mapping.',
    'Generate a learning path.',
    'Build an authorized workflow plan.',
    'Route a task to A/B/C/D.',
    'Run benchmark.',
    'Generate agent readiness report.',
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
        <h1>Security Knowledge Base &amp; Agent Memory Lab · v3.0-rc</h1>
        <p>Local cybersecurity knowledge base, retrieval, safety policy, agent memory, task routing, and benchmark platform.</p>
      </header>
      <HealthCard />
      <DisclosureCard />
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
      <ReviewerQuickPath />
      <p className="muted" style={{ textAlign: 'center', margin: '24px 0' }}>
        Local-only. No real targets. No real API keys. No real scanning.
      </p>
    </div>
  )
}
