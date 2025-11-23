import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import federation from '@originjs/vite-plugin-federation'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'host-app',
      remotes: {
        // In dev, these run on different ports.
        // In prod, these would be full URLs to built assets.
        emr: 'http://localhost:3001/assets/remoteEntry.js',
        pos: 'http://localhost:3002/assets/remoteEntry.js',
      },
      shared: ['vue', 'pinia', 'vue-router']
    })
  ],
  build: {
    target: 'esnext' // Required for Top-level await in federation
  },
  server: {
    port: 3000
  }
})
