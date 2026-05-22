import React, { useState } from 'react'
import { alignDepartment } from '../services/api.js'

export default function AlignmentForm({ onResult, onError }) {
  const [department, setDepartment] = useState('computer_science')
  const [corporate, setCorporate] = useState('apple')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    onError(null)
    onResult(null)

    try {
      const data = await alignDepartment(department, corporate)
      onResult(data)
    } catch (err) {
      onError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const selectStyle = { padding: '0.5rem', borderRadius: '0.25rem', border: '1px solid #d1d5db', marginRight: '1rem' }

  return (
    <form onSubmit={handleSubmit} style={{ background: '#f3f4f6', padding: '1.5rem', borderRadius: '0.5rem' }}>
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>Department</label>
          <select value={department} onChange={e => setDepartment(e.target.value)} style={selectStyle}>
            <option value="computer_science">Computer Science</option>
            <option value="public_health">Public Health</option>
            <option value="business">Business</option>
            <option value="psychology">Psychology</option>
            <option value="english">English</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>Corporate Partner</label>
          <select value={corporate} onChange={e => setCorporate(e.target.value)} style={selectStyle}>
            <option value="apple">Apple</option>
            <option value="google">Google</option>
            <option value="pfizer">Pfizer</option>
          </select>
        </div>

        <div style={{ marginTop: '1.5rem' }}>
          <button type="submit" disabled={loading} style={{ padding: '0.5rem 1.5rem', background: '#2563eb', color: 'white', border: 'none', borderRadius: '0.25rem', cursor: loading ? 'not-allowed' : 'pointer' }}>
            {loading ? 'Aligning...' : 'Align'}
          </button>
        </div>
      </div>
    </form>
  )
}
