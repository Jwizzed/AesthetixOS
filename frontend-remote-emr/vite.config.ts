import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import federation from '@originjs/vite-plugin-federation'

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'emr',
      filename: 'remoteEntry.js',
      exposes: {
        './PatientModule': './src/views/PatientModule.vue'
      },
      shared: ['vue', 'pinia']
    })
  ],
  build: {
    target: 'esnext'
  },
  server: {
    port: 3001,
    origin: 'http://localhost:3001',
    cors: true
  },
  preview: {
    port: 3001,
    strictPort: true,
    cors: true
  },
  base: 'http://localhost:3001/'
})
