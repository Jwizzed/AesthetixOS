import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import federation from '@originjs/vite-plugin-federation'

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'pos',
      filename: 'remoteEntry.js',
      exposes: {
        './BillingModule': './src/views/BillingModule.vue'
      },
      shared: ['vue', 'pinia']
    })
  ],
  build: {
    target: 'esnext'
  },
  server: {
    port: 3002,
    origin: 'http://localhost:3002',
    cors: true
  },
  preview: {
    port: 3002,
    strictPort: true,
    cors: true
  },
  base: 'http://localhost:3002/'
})
