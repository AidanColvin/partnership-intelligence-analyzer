import React, { useState } from 'react';
export default function App() {
  const [c, setC] = useState('');
  const [res, setRes] = useState(null);
  const submit = async (e) => {
    e.preventDefault();
    const r = await fetch('http://localhost:8000/api/align', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({companyName: c})
    });
    setRes(await r.json());
  };
  return (
    <div style={{padding: '50px'}}>
      <h1>Partnership Analyzer</h1>
      <form onSubmit={submit}>
        <input onChange={(e) => setC(e.target.value)} placeholder="Type 'apple'" />
        <button type="submit">Analyze</button>
      </form>
      {res && <pre>{JSON.stringify(res, null, 2)}</pre>}
    </div>
  );
}
