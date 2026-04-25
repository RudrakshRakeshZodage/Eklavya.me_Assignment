'use client';

import { useState, useEffect } from 'react';
import styles from './page.module.css';

interface MCQ {
  question: string;
  options: string[];
  answer: string;
}

interface WorkflowStep {
  agent: string;
  status: 'success' | 'fail' | 'pass';
  feedback?: string[];
}

interface Content {
  explanation: string;
  mcqs: MCQ[];
}

interface PipelineResponse {
  workflow: WorkflowStep[];
  final_content: Content;
}

export default function Home() {
  const [isMounted, setIsMounted] = useState(false);
  const [grade, setGrade] = useState(4);
  const [topic, setTopic] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<PipelineResponse | null>(null);
  const [error, setError] = useState('');
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const triggerPipeline = async () => {
    setLoading(true);
    setError('');
    setData(null);
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [`[${timestamp}] Initiating pipeline for: ${topic}`, ...prev]);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grade, topic })
      });

      const result = await response.json();
      console.log("PIPELINE RESULT:", result);
      
      if (!response.ok) {
        const errorMsg = result.detail || result.error || 'System error during generation';
        setLogs(prev => [`[${new Date().toLocaleTimeString()}] ERROR: ${errorMsg}`, ...prev]);
        throw new Error(errorMsg);
      }

      setLogs(prev => [`[${new Date().toLocaleTimeString()}] Pipeline completed successfully.`, ...prev]);
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isMounted) return null;

  return (
    <div className={styles.dashboard}>
      <aside className={styles.sidebar}>
        <div className={styles.logoBox}>E.</div>
        <div style={{ marginTop: 'auto', marginBottom: '2rem', fontWeight: 900, fontSize: '0.8rem' }}>V2.1</div>
      </aside>

      <header className={styles.topbar}>
        <div className={styles.pageTitle}>✦ AI Learning Architect / Control Center</div>
        <div style={{ fontWeight: 800, color: '#64748b' }}>
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.header}>
          <h1 className={styles.title}>Welcome back, <span style={{ color: '#6366f1' }}>Designer</span></h1>
          <p style={{ color: '#64748b', fontWeight: 700, marginTop: '0.5rem' }}>
            {new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric' })}
          </p>
        </div>

        <div className={styles.statsGrid}>
          <div className={styles.statCard} style={{ borderTop: '6px solid #fbbf24' }}>
            <div className={styles.statLabel}>Active Agents</div>
            <div className={styles.statValue}>2.0</div>
          </div>
          <div className={styles.statCard} style={{ borderTop: '6px solid #6366f1' }}>
            <div className={styles.statLabel}>Target Level</div>
            <div className={styles.statValue}>G-{grade}</div>
          </div>
          <div className={styles.statCard} style={{ borderTop: '6px solid #10b981' }}>
            <div className={styles.statLabel}>Pipeline Status</div>
            <div className={styles.statValue}>{loading ? 'BUSY' : 'IDLE'}</div>
          </div>
          <div className={styles.statCard} style={{ borderTop: '6px solid #000' }}>
            <div className={styles.statLabel}>Engine</div>
            <div className={styles.statValue}>Multi-AI</div>
          </div>
        </div>

        <section className={styles.inputArea}>
          <div className={styles.inputField} style={{ flex: 1 }}>
            <label>Choose Grade</label>
            <select value={grade} onChange={(e) => setGrade(Number(e.target.value))}>
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(g => (
                <option key={g} value={g}>Grade {g}</option>
              ))}
            </select>
          </div>
          <div className={styles.inputField} style={{ flex: 3 }}>
            <label>Topic to Master</label>
            <input 
              type="text" 
              placeholder="e.g. 4G Technology, Solar System..." 
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          <button 
            className={styles.generateBtn} 
            onClick={triggerPipeline}
            disabled={loading || !topic}
          >
            {loading ? 'Processing...' : 'Run Pipeline ⚡'}
          </button>
        </section>

        {error && (
          <div className={styles.error} style={{ marginBottom: '2rem' }}>
            <div style={{ fontWeight: 900 }}>⚠️ BRIDGE ALERT</div>
            <div style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.8 }}>{error}</div>
          </div>
        )}

        {loading && (
          <div className="animate-fade-in" style={{ display: 'flex', alignItems: 'center', gap: '2rem', background: '#fff', padding: '2rem', border: '4px solid #000', boxShadow: '10px 10px 0px #fbbf24', marginBottom: '3rem' }}>
            <div className={styles.loader}></div>
            <div>
              <div style={{ fontWeight: 900, textTransform: 'uppercase', fontSize: '1.2rem' }}>Agent Collaboration in Progress</div>
              <div style={{ color: '#64748b', fontWeight: 600 }}>Switching providers and verifying curriculum...</div>
            </div>
          </div>
        )}

        {/* Bridge Activity Section */}
        <section className={styles.card} style={{ marginBottom: '3rem', background: '#0f172a', color: '#38bdf8', border: 'none' }}>
          <div className={styles.stepHeader} style={{ marginBottom: '1.5rem', borderBottom: '1px solid #1e293b', paddingBottom: '1rem' }}>
            <span style={{ fontWeight: 900, letterSpacing: '0.1em', color: '#fff' }}>LIVE BRIDGE ACTIVITY</span>
            <span style={{ fontSize: '0.7rem', background: '#0ea5e9', color: '#fff', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>CONNECTED</span>
          </div>
          <div style={{ fontFamily: 'monospace', fontSize: '0.85rem', maxHeight: '150px', overflowY: 'auto' }}>
            {logs.length === 0 && <div style={{ color: '#64748b' }}>Waiting for connection...</div>}
            {logs.map((log, i) => (
              <div key={i} style={{ marginBottom: '0.5rem', display: 'flex', gap: '1rem' }}>
                <span style={{ color: '#64748b', whiteSpace: 'nowrap' }}>{log.split('] ')[0]}]</span>
                <span style={{ color: log.includes('ERROR') ? '#f43f5e' : (log.includes('successfully') ? '#10b981' : '#38bdf8') }}>
                  {log.split('] ')[1]}
                </span>
              </div>
            ))}
          </div>
        </section>

        {data && (
          <div className={`${styles.contentGrid} animate-fade-in`}>
            <aside className={styles.card}>
              <h2 className={styles.sectionTitle}>Agent Pulse</h2>
              <div className={styles.workflowList}>
                {data.workflow?.map((step, i) => (
                  <div key={i} className={styles.workflowStep}>
                    <div className={styles.stepHeader}>
                      <span>{step.agent}</span>
                      <span className={styles[step.status]}>{step.status}</span>
                    </div>
                    {step.feedback && (
                      <ul style={{ fontSize: '0.85rem', marginTop: '0.8rem', color: '#64748b', paddingLeft: '1rem' }}>
                        {step.feedback.map((f, j) => <li key={j}>{f}</li>)}
                      </ul>
                    )}
                  </div>
                ))}
              </div>
            </aside>

            <main className={styles.card}>
              <h2 className={styles.sectionTitle} style={{ background: '#6366f1' }}>Master Brief</h2>
              <div style={{ marginBottom: '3rem', background: '#f8fafc', padding: '2rem', border: '2px solid #000' }}>
                <p style={{ lineHeight: 1.8, fontSize: '1.15rem', color: '#1e293b' }}>
                  {data.final_content?.explanation || 'No content generated.'}
                </p>
              </div>

              <h2 className={styles.sectionTitle} style={{ background: '#10b981' }}>Assessment Suite</h2>
              <div className={styles.mcqGrid}>
                {data.final_content?.mcqs?.map((mcq, i) => (
                  <div key={i} className={styles.mcqCard}>
                    <p style={{ fontWeight: 800, marginBottom: '1rem' }}>{mcq.question}</p>
                    <div className={styles.options}>
                      {mcq.options.map((opt, j) => (
                        <div key={j} className={styles.option}>{opt}</div>
                      ))}
                    </div>
                    <div className={styles.answer}>✓ {mcq.answer}</div>
                  </div>
                ))}
              </div>
            </main>
          </div>
        )}
      </main>
    </div>
  );
}
