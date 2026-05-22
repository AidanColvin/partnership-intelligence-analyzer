import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../src/App'

global.fetch = vi.fn()

test('backend error shows user-friendly message', async () => {
  fetch.mockResolvedValueOnce({
    ok: false,
    json: async () => ({ detail: 'Unknown department' })
  })

  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: /Align/i }))

  await waitFor(() => {
    expect(screen.getByTestId('error-state')).toBeDefined()
  })

  expect(screen.getByText(/Unknown department/i)).toBeDefined()
})
