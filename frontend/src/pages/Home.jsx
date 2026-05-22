import React, { useState } from 'react'
import AlignmentForm from '../components/AlignmentForm.jsx'

export default function Home() {
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <AlignmentForm onResult={setResult} onError={setError} />
      
      {error && (
        <div data-testid="error-state" style={{ padding: '1rem', background: '#fee2e2', color: '#991b1b', borderRadius: '0.5rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div data-testid="result-state" style={{ padding: '1.5rem', background: '#ffffff', border: '1px solid #e5e7eb', borderRadius: '0.5rem' }}>
          <h2 style={{ marginTop: 0 }}>Results</h2>
          <p><strong>Partner:</strong> {result.corporate_slug}</p>
          <p><strong>Department:</strong> {result.department_id}</p>
          <div style={{ fontSize: '1.5rem', color: '#2563eb', margin: '1rem 0' }}>
            <strong>Score: {result.score}%</strong>
          </div>
          <ul>
            <li>Intensity Metric: {result.intensity_metric}</li>
            <li>Matches Found: {result.match_count}</li>
            <li>Total Words: {result.word_count}</li>
          </ul>
        </div>
      )}
    </div>
  )
}
