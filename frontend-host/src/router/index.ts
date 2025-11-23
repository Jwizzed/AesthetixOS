import { createRouter, createWebHistory } from 'vue-router'

// Lazy load remotes
const PatientModule = () => import('emr/PatientModule')
const BillingModule = () => import('pos/BillingModule')

// Temporary local placeholders (Fallback if remote fails)
const Dashboard = { template: '<div class="p-4 bg-white rounded shadow">Welcome to the Dashboard. Select a module.</div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/emr', component: PatientModule }, 
    { path: '/pos', component: BillingModule },
  ]
})

export default router


