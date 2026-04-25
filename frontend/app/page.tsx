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

  useEffect(() => {
    setIsMounted(true);
  }, []);

  const triggerPipeline = async () => {
    setLoading(true);
    setError('');
    setData(null);

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grade, topic })
      });

      const result = await response.json();
      console.log("PIPELINE RESULT:", result);
      
      if (!response.ok) {
        throw new Error(result.error || 'System error during generation');
      }

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

        {error && <div className={styles.error} style={{ marginBottom: '2rem' }}>⚠️ SYSTEM ALERT: {error}</div>}

        {loading && (
          <div className="animate-fade-in" style={{ display: 'flex', alignItems: 'center', gap: '2rem', background: '#fff', padding: '2rem', border: '4px solid #000', boxShadow: '10px 10px 0px #fbbf24', marginBottom: '3rem' }}>
            <div className={styles.loader}></div>
            <div>
              <div style={{ fontWeight: 900, textTransform: 'uppercase', fontSize: '1.2rem' }}>Agent Collaboration in Progress</div>
              <div style={{ color: '#64748b', fontWeight: 600 }}>Switching providers and verifying curriculum...</div>
            </div>
          </div>
        )}

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
