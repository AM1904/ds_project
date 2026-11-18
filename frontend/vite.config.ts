import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Dev: Vite serves the UI on :5173 and forwards /api to Flask (default :5050, override with API_TARGET).
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { '/api': process.env.API_TARGET ?? 'http://localhost:5050' } },
  build: { outDir: 'dist', sourcemap: false },
});
