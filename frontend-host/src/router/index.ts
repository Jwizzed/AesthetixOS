import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import ErrorLoad from '../views/ErrorLoad.vue'

// Lazy load remotes
// Note: These must match the keys in vite.config.ts remotes
const PatientModule = () => import('emr/PatientModule').catch((err) => {
  console.error('Failed to load EMR Remote:', err);
  return ErrorLoad;
})
const BillingModule = () => import('pos/BillingModule').catch((err) => {
  console.error('Failed to load POS Remote:', err);
  return ErrorLoad;
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/emr', component: PatientModule }, 
    { path: '/pos', component: BillingModule },
  ]
})

export default router


