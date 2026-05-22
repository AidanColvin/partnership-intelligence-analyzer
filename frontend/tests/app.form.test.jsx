import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../src/App'

global.fetch = vi.fn()

test('submitting form triggers API call and shows results', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      department_id: 'computer_science',
      corporate_slug: 'apple',
      score: 85.5,
      intensity_metric: 855.0,
      word_count: 100,
      match_count: 5
    })
  })

  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: /Align/i }))

  await waitFor(() => {
    expect(screen.getByTestId('result-state')).toBeDefined()
  })

  expect(screen.getByText(/Score: 85.5%/i)).toBeDefined()
})
