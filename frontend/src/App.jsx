import React from 'react'
import Home from './pages/Home.jsx'

export default function App() {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ color: '#111827' }}>UNC-Industry Alignment Engine</h1>
      </header>
      <main>
        <Home />
      </main>
    </div>
  )
}
