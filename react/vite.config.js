import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/all': 'https://sizning-loyiha-nomingiz.onrender.com',
      '/create': 'https://sizning-loyiha-nomingiz.onrender.com',
      '/update': 'https://sizning-loyiha-nomingiz.onrender.com',
      '/delete': 'https://sizning-loyiha-nomingiz.onrender.com',
    }
  }
})
