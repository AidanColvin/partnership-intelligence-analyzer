const API_BASE = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export const alignDepartment = async (departmentId, corporateSlug) => {
  const response = await fetch(`${API_BASE}/api/align`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      department_id: departmentId,
      corporate_slug: corporateSlug
    })
  })

  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.detail || 'Failed to align partner data')
  }

  return data
}
