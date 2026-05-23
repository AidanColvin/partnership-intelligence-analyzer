import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/partnership-intelligence-analyzer/',
  server: { port: 3000 }
});
