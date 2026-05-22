import React from 'react'
import { render, screen } from '@testing-library/react'
import App from '../src/App'

test('renders heading and form elements', () => {
  render(<App />)
  // Matching the hyphen used in App.jsx
  expect(screen.getByText('UNC-Industry Alignment Engine')).toBeDefined()
  expect(screen.getByText('Department')).toBeDefined()
  expect(screen.getByText('Corporate Partner')).toBeDefined()
  expect(screen.getByRole('button', { name: /Align/i })).toBeDefined()
})
