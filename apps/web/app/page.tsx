"use client";
import React from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  return (
    <main style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '100vh',
      padding: '2rem', 
      textAlign: 'center', 
      fontFamily: 'sans-serif',
      backgroundColor: '#f9fafb'
    }}>
      <h1 style={{ fontSize: '3rem', color: '#111827', marginBottom: '1rem' }}>NiveshGuard</h1>
      <p style={{ fontSize: '1.2rem', color: '#6b7280', marginBottom: '3rem', maxWidth: '600px' }}>
        Understand. Verify. Pause. Protect. <br/>
        The safety layer between you and suspicious financial messages.
      </p>
      
      <div style={{ display: 'flex', gap: '1rem' }}>
        <button 
          onClick={() => router.push('/check')}
          style={{ 
            padding: '1rem 2rem', 
            fontSize: '1.1rem', 
            fontWeight: 'bold',
            backgroundColor: '#2563eb', 
            color: 'white', 
            border: 'none', 
            borderRadius: '8px', 
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}
        >
          Check Something
        </button>
        <button 
          style={{ 
            padding: '1rem 2rem', 
            fontSize: '1.1rem', 
            backgroundColor: 'white', 
            color: '#374151', 
            border: '1px solid #ddd', 
            borderRadius: '8px', 
            cursor: 'pointer' 
          }}
        >
          I've already acted
        </button>
      </div>
    </main>
  );
}
