<template>
  <div class="space-y-6 lg:space-y-10">
    <!-- Hero Section -->
    <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6 lg:p-10 shadow-2xl shadow-slate-900/10">
        <div class="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-brand-500/20 rounded-full blur-3xl"></div>
        <div class="absolute bottom-0 left-0 -mb-20 -ml-20 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
        
        <div class="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
                <h2 class="text-2xl lg:text-4xl font-bold text-white tracking-tight mb-2">Good Morning, Dr. Smith</h2>
                <p class="text-slate-400 text-base lg:text-lg">You have <strong class="text-white">12 appointments</strong> today. Next one starts in 15 mins.</p>
            </div>
            <button class="w-full md:w-auto px-6 py-3 bg-white/10 backdrop-blur-md border border-white/20 text-white rounded-xl font-medium hover:bg-white/20 transition-all">
                View Calendar
            </button>
        </div>
    </div>
    
    <!-- Key Metrics -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6">
        <div v-for="(stat, i) in stats" :key="i" class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-lg hover:border-brand-100 transition-all duration-300 group">
            <div class="flex justify-between items-start mb-4">
                <div class="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300" :class="stat.bgClass">
                    {{ stat.icon }}
                </div>
                <span class="text-xs font-bold px-2 py-1 rounded-full" :class="stat.trend > 0 ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'">
                    {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
                </span>
            </div>
            <div class="text-3xl font-bold text-slate-900 mb-1">{{ stat.value }}</div>
            <div class="text-sm text-slate-500 font-medium">{{ stat.label }}</div>
        </div>
    </div>

    <!-- Main Modules Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 lg:gap-8">
       <!-- EMR Card -->
      <router-link to="/emr" class="group relative overflow-hidden bg-white p-6 lg:p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-2xl hover:shadow-brand-900/5 hover:border-brand-200 transition-all duration-500 flex flex-col">
        <div class="absolute top-0 right-0 w-64 h-64 bg-brand-50/50 rounded-full -mr-32 -mt-32 group-hover:bg-brand-100/50 transition-colors duration-500"></div>
        
        <div class="relative z-10 mb-8">
            <div class="w-16 h-16 bg-brand-100 text-brand-600 rounded-2xl flex items-center justify-center text-3xl mb-6 shadow-lg shadow-brand-500/20 group-hover:rotate-6 transition-transform duration-500">
                📋
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-3 group-hover:text-brand-600 transition-colors">Medical Records</h3>
            <p class="text-slate-500 text-lg leading-relaxed">
                Comprehensive patient management. Access histories, face charts, and diagnosis tools in one unified interface.
            </p>
        </div>
        
        <div class="mt-auto pt-6 border-t border-slate-50 flex items-center text-brand-600 font-bold group-hover:translate-x-2 transition-transform">
            <span>Launch Module</span>
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </div>
      </router-link>
      
      <!-- POS Card -->
      <router-link to="/pos" class="group relative overflow-hidden bg-white p-6 lg:p-8 rounded-3xl shadow-sm border border-slate-100 hover:shadow-2xl hover:shadow-brand-900/5 hover:border-brand-200 transition-all duration-500 flex flex-col">
        <div class="absolute top-0 right-0 w-64 h-64 bg-blue-50/50 rounded-full -mr-32 -mt-32 group-hover:bg-blue-100/50 transition-colors duration-500"></div>
        
        <div class="relative z-10 mb-8">
            <div class="w-16 h-16 bg-blue-100 text-blue-600 rounded-2xl flex items-center justify-center text-3xl mb-6 shadow-lg shadow-blue-500/20 group-hover:-rotate-6 transition-transform duration-500">
                💳
            </div>
            <h3 class="text-2xl font-bold text-slate-900 mb-3 group-hover:text-blue-600 transition-colors">Point of Sale</h3>
            <p class="text-slate-500 text-lg leading-relaxed">
                Smart billing and inventory. Process payments, track commissions, and manage stock with ease.
            </p>
        </div>
        
        <div class="mt-auto pt-6 border-t border-slate-50 flex items-center text-blue-600 font-bold group-hover:translate-x-2 transition-transform">
            <span>Launch Module</span>
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
        </div>
      </router-link>
    </div>

    <!-- Recent Activity Table -->
    <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="p-6 border-b border-slate-50 flex justify-between items-center">
            <h3 class="font-bold text-slate-800 text-lg">Recent Transactions</h3>
            <button @click="fetchActivity" class="text-sm text-brand-600 font-medium hover:text-brand-700 flex items-center gap-1">
                <span v-if="loading" class="animate-spin">↻</span>
                Refresh
            </button>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full min-w-[600px]">
                <thead class="bg-slate-50/50">
                    <tr>
                        <th class="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Time</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Patient</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Action</th>
                        <th class="px-6 py-4 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Status</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                    <tr v-if="activities.length === 0 && !loading" class="text-center text-slate-500">
                        <td colspan="4" class="py-8">No recent activity found.</td>
                    </tr>
                    <tr v-for="item in activities" :key="item.id" class="hover:bg-slate-50/50 transition-colors">
                        <td class="px-6 py-4 text-sm text-slate-500">{{ item.time }}</td>
                        <td class="px-6 py-4 text-sm font-medium text-slate-900 flex items-center gap-3">
                            <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold text-slate-500">
                                {{ item.patientName.charAt(0) }}
                            </div>
                            {{ item.patientName }}
                        </td>
                        <td class="px-6 py-4 text-sm text-slate-600">{{ item.action }}</td>
                        <td class="px-6 py-4">
                            <span class="px-3 py-1 rounded-full text-xs font-bold" :class="item.statusClass">
                                {{ item.status }}
                            </span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = [
    { label: 'Total Revenue', value: '฿124,500', icon: '💰', bgClass: 'bg-green-50 text-green-600', trend: 12.5 },
    { label: 'Appointments', value: '48', icon: '📅', bgClass: 'bg-blue-50 text-blue-600', trend: 8.2 },
    { label: 'New Patients', value: '15', icon: '👥', bgClass: 'bg-purple-50 text-purple-600', trend: -2.4 },
    { label: 'Inventory Alerts', value: '3', icon: '⚠️', bgClass: 'bg-orange-50 text-orange-600', trend: 0 },
]

interface Activity {
    id: string
    time: string
    patientName: string
    patientId: string
    action: string
    status: string
    statusClass: string
}

const activities = ref<Activity[]>([])
const loading = ref(false)

const fetchActivity = async () => {
    loading.value = true
    try {
        // 1. Fetch Transactions (Commerce)
        const trxRes = await axios.get('http://localhost:8000/api/v1/commerce/transactions/')
        // 2. Fetch Patients (Clinic)
        const patRes = await axios.get('http://localhost:8000/api/v1/clinic/patients/')
        
        const patientsMap = new Map(patRes.data.map((p: any) => [p.id, `${p.first_name} ${p.last_name}`]))

        // Map transactions to activity format
        const transactionActivities = trxRes.data.map((t: any) => ({
            id: t.id,
            time: new Date(t.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            patientId: t.patient,
            patientName: patientsMap.get(t.patient) || 'Unknown Patient',
            action: `Payment: ฿${Number(t.total_amount).toLocaleString()}`,
            status: t.status,
            statusClass: t.status === 'COMPLETED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
        }))

        // Sort by newest
        activities.value = transactionActivities.reverse().slice(0, 10)

    } catch (error) {
        console.error('Failed to fetch activity', error)
        // Fallback mock data if API fails
        activities.value = [
            { id: '1', time: '10:30 AM', patientName: 'Mock Patient', patientId: '1', action: 'System Offline Mode', status: 'Error', statusClass: 'bg-red-100 text-red-700' }
        ]
    } finally {
        loading.value = false
    }
}

onMounted(() => {
    fetchActivity()
})
</script>