import React from 'react'
import { render, screen } from '@testing-library/react'
import App from '../src/App'

test('home page renders form controls and submit button', () => {
  render(<App />)
  expect(screen.getByText('UNC-Industry Alignment Engine')).toBeDefined()
  expect(screen.getByText('Department')).toBeDefined()
  expect(screen.getByText('Corporate Partner')).toBeDefined()
  expect(screen.getByRole('button', { name: /Align/i })).toBeDefined()
})
