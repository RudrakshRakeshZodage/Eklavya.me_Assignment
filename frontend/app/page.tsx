'use client';

import { useState } from 'react';
import styles from './page.module.css';

interface MCQ {
  question: string;
  options: string[];
  answer: string;
}

interface Content {
  explanation: string;
  mcqs: MCQ[];
}

interface AgentStep {
  agent: string;
  status: string;
  output: any;
  feedback?: string[];
}

interface WorkflowResponse {
  workflow: AgentStep[];
  final_content: Content;
}

export default function Home() {
  const [grade, setGrade] = useState<number>(4);
  const [topic, setTopic] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<WorkflowResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const triggerPipeline = async () => {
    if (!topic) return;
    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grade, topic }),
      });

      if (!response.ok) throw new Error('Failed to generate content');

      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header className={styles.header}>
        <h1 className={styles.title}>AI Learning <span className={styles.gradientText}>Architect</span></h1>
        <p className={styles.subtitle}>Agent-based educational content generation and review</p>
      </header>

      <section className="glass-card animate-fade-in">
        <div className={styles.inputGroup}>
          <div className={styles.inputField}>
            <label>Target Grade</label>
            <select value={grade} onChange={(e) => setGrade(Number(e.target.value))}>
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(g => (
                <option key={g} value={g}>Grade {g}</option>
              ))}
            </select>
          </div>
          <div className={styles.inputField} style={{ flex: 2 }}>
            <label>Topic</label>
            <input 
              type="text" 
              placeholder="e.g. Types of angles, Solar System, Fractions..." 
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
          </div>
          <button 
            className={styles.generateBtn} 
            onClick={triggerPipeline}
            disabled={loading || !topic}
          >
            {loading ? 'Processing...' : 'Generate Content'}
          </button>
        </div>
      </section>

      {error && <div className={styles.error}>{error}</div>}

      {loading && (
        <div className={styles.loaderContainer}>
          <div className={styles.loader}></div>
          <p>Agents are collaborating...</p>
        </div>
      )}

      {data && (
        <div className={styles.contentGrid}>
          {/* Workflow Visualization */}
          <section className="glass-card animate-fade-in">
            <h2 className={styles.sectionTitle}>Agent Workflow</h2>
            <div className={styles.workflowList}>
              {data.workflow.map((step, i) => (
                <div key={i} className={`${styles.workflowStep} ${styles[step.status]}`}>
                  <div className={styles.stepHeader}>
                    <span className={styles.agentName}>{step.agent}</span>
                    <span className={styles.stepStatus}>{step.status.toUpperCase()}</span>
                  </div>
                  {step.feedback && step.feedback.length > 0 && (
                    <ul className={styles.feedbackList}>
                      {step.feedback.map((f, j) => <li key={j}>{f}</li>)}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </section>

          {/* Final Content Display */}
          <section className="glass-card animate-fade-in" style={{ gridColumn: 'span 2' }}>
            <h2 className={styles.sectionTitle}>Generated Content</h2>
            <div className={styles.explanationBox}>
              <h3>Explanation</h3>
              <p>{data.final_content.explanation}</p>
            </div>
            
            <div className={styles.mcqGrid}>
              {data.final_content.mcqs.map((mcq, i) => (
                <div key={i} className={styles.mcqCard}>
                  <h4>Question {i + 1}</h4>
                  <p>{mcq.question}</p>
                  <div className={styles.options}>
                    {mcq.options.map((opt, j) => (
                      <div key={j} className={styles.option}>
                        {opt}
                      </div>
                    ))}
                  </div>
                  <div className={styles.answer}>Correct Answer: {mcq.answer}</div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </main>
  );
}
