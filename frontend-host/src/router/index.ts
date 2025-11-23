import { createRouter, createWebHistory } from 'vue-router'

// Lazy load remotes
// Note: We need to configure the remotes to expose these components first.
// For now, we will place placeholders or try to import them.
// const PatientModule = () => import('emr/PatientModule')
// const BillingModule = () => import('pos/BillingModule')

// Temporary local placeholders until remotes are built
const Dashboard = { template: '<div class="p-4 bg-white rounded shadow">Welcome to the Dashboard. Select a module.</div>' }
const EMRPlaceholder = { template: '<div class="p-4 border-2 border-dashed border-blue-300 rounded text-blue-600">EMR Module Loading... (Remote)</div>' }
const POSPlaceholder = { template: '<div class="p-4 border-2 border-dashed border-green-300 rounded text-green-600">POS Module Loading... (Remote)</div>' }

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    // Real implementation will swap these components with the federated imports
    { path: '/emr', component: EMRPlaceholder }, 
    { path: '/pos', component: POSPlaceholder },
  ]
})

export default router


