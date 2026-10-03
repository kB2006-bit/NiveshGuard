"use client";
import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { t, Language } from '../lib/i18n';

export default function VerifyPage() {
  const params = useParams();
  const router = useRouter();
  const [lang, setLang] = useState<Language>('en');
  const [state, setState] = useState<'BEFORE_ACTION' | 'UNCERTAIN' | 'AFTER_ACTION'>('BEFORE_ACTION');
  const [workflow, setWorkflow] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchWorkflow = async (selectedState: string) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('state', selectedState);
      formData.append('session_id', params.sessionId as string);
      
      const res = await fetch('/api/verify/workflow', { method: 'POST', body: formData });
      const data = await res.json();
      setWorkflow(data.workflow);
    } catch (e) {
      alert("Failed to load safety workflow.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWorkflow(state);
  }, [state]);

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
        <select value={lang} onChange={(e) => setLang(e.target.value as Language)}>
          <option value="en">English</option>
          <option value="hi">हिन्दी</option>
          <option value="mr">मराठी</option>
        </select>
        <button onClick={() => router.push('/results/' + params.sessionId)} style={{ cursor: 'pointer' }}>Back to Results</button>
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginBottom: '3rem' }}>
        {['BEFORE_ACTION', 'UNCERTAIN', 'AFTER_ACTION'].map((s) => (
          <button 
            key={s} 
            onClick={() => setState(s as any)}
            style={{ 
              padding: '0.5rem 1rem', 
              borderRadius: '8px', 
              border: '1px solid #ddd', 
              cursor: 'pointer', 
              backgroundColor: state === s ? '#2563eb' : '#fff',
              color: state === s ? 'white' : 'black'
            }}
          >
            {s.replace('_', ' ')}
          </button>
        ))}
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem' }}>Generating your safety plan...</div>
      ) : workflow ? (
        <div style={{ backgroundColor: '#fff', padding: '2rem', borderRadius: '12px', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
          {state === 'BEFORE_ACTION' && (
            <div>
              <h2 style={{ color: '#b91c1b' }}>Warning: Pause Before You Act</h2>
              <p style={{ fontSize: '1.1rem', marginBottom: '2rem' }}>{workflow.primary_message}</p>
              {workflow.sensitive_data_warning && (
                <div style={{ backgroundColor: '#fee2e2', color: '#b91c1b', padding: '1rem', borderRadius: '8px', marginBottom: '2rem', fontWeight: 'bold' }}>
                  WARNING: This communication asks for sensitive data (OTP/PIN). NEVER share these.
                </div>
              )}
              <h3>Verification Checklist</h3>
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {workflow.checklist.map((item: any, i: number) => (
                  <li key={i} style={{ padding: '1rem', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between' }}>
                    <span>{item.item}</span>
                    <span style={{ fontSize: '0.8rem', color: '#6b7280' }}>Source: {item.source}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {state === 'UNCERTAIN' && (
            <div>
              <h2 style={{ color: '#d97706' }}>Clarifying the Situation</h2>
              <p style={{ marginBottom: '2rem' }}>{workflow.cautionary_note}</p>
              <h3>Missing Evidence</h3>
              <ul>
                {workflow.missing_evidence.map((item: string, i: number) => (
                  <li key={i}>{item}</li>
                ))}
              </ul>
              <h3>Recommended Next Steps</h3>
              <ul>
                {workflow.verification_steps.map((step: string, i: number) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
            </div>
          )}

          {state === 'AFTER_ACTION' && (
            <div>
              <h2 style={{ color: '#4b5563' }}>Incident Documentation</h2>
              <div style={{ backgroundColor: '#f3f4f6', padding: '1.5rem', borderRadius: '8px', marginBottom: '2rem', whiteSpace: 'pre-wrap' }}>
                {workflow.incident_summary}
              </div>
              <h3>Official Reporting Channels</h3>
              <div style={{ display: 'grid', gap: '1rem' }}>
                {workflow.reporting_pathways.map((p: any, i: number) => (
                  <div key={i} style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
                    <div style={{ fontWeight: 'bold' }}>{p.channel}</div>
                    <div style={{ fontSize: '0.9rem' }}>{p.instruction}</div>
                    <a href={p.url} target="_blank" rel="noopener noreferrer" style={{ color: '#2563eb', fontSize: '0.8rem' }}>Visit Official Site</a>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '4rem' }}>No workflow available.</div>
      )}
    </div>
  );
}
