<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import FaceCanvas from '../components/FaceCanvas.vue'
import axios from 'axios'

// Setup API
const api = axios.create({ baseURL: 'http://localhost:8000/api/v1/clinic/' })

const patient = ref<any>(null)
const sessions = ref<any[]>([])
const loading = ref(true)
const sessionsLoading = ref(false)
const error = ref('')
const activeTab = ref('face-chart')

const tabs = [
    { id: 'overview', label: 'Overview', icon: '👤' },
    { id: 'face-chart', label: 'Face Chart', icon: '🎨' },
    { id: 'history', label: 'History', icon: '🕒' },
    { id: 'notes', label: 'Doctor Notes', icon: '📝' }
]

const fetchSessions = async () => {
    if (!patient.value?.id) return
    sessionsLoading.value = true
    try {
        const response = await api.get(`sessions/?patient=${patient.value.id}`)
        sessions.value = response.data
    } catch (e) {
        console.error('Failed to fetch sessions', e)
    } finally {
        sessionsLoading.value = false
    }
}

watch(activeTab, (newTab) => {
    if (newTab === 'history') {
        fetchSessions()
    }
})

onMounted(async () => {
  try {
    // Hardcoded ID for demo purposes - normally comes from route/prop
    const response = await api.get('patients/')
    if (response.data && response.data.length > 0) {
      patient.value = response.data[0] 
      // Prefetch sessions if needed, but let's do it on tab switch or if patient loaded
      if (activeTab.value === 'history') fetchSessions()
    } else {
        // Fallback Mock Data if API fails or returns empty
         console.warn('API failed or empty, using mock data for demo')
         patient.value = {
            id: '999',
            first_name: "Jane",
            last_name: "Doe",
            hn: "66-00123",
            phone_number: "081-234-5678",
            date_of_birth: "1995-08-15"
         }
    }
  } catch (e) {
    console.warn('Failed to load patient data, using mock fallback for demo.', e)
    // Mock fallback so UI always looks good for demo
    patient.value = {
        id: '999',
        first_name: "Jane",
        last_name: "Doe",
        hn: "66-00123",
        phone_number: "081-234-5678",
        date_of_birth: "1995-08-15"
    }
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="flex flex-col lg:flex-row h-auto lg:h-[calc(100vh-7rem)] gap-6 overflow-hidden lg:overflow-hidden">
    <!-- Left Sidebar: Patient List & Selection (Mocked as "Current Patient" context) -->
    <aside class="w-full lg:w-80 flex-shrink-0 flex flex-col gap-6">
        <!-- Patient Card -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 relative overflow-hidden group">
            <div class="absolute top-0 left-0 w-full h-24 bg-gradient-to-b from-brand-50 to-transparent"></div>
            
            <div v-if="loading" class="text-center py-10 text-slate-400">Loading...</div>
            <div v-else-if="error" class="text-center py-10 text-red-500">{{ error }}</div>
            <div v-else-if="patient" class="relative z-10 flex flex-col items-center text-center">
                <div class="w-24 h-24 rounded-full bg-white p-1 shadow-lg mb-4">
                    <div class="w-full h-full rounded-full bg-slate-100 flex items-center justify-center text-3xl font-bold text-slate-400">
                        {{ patient.first_name[0] }}{{ patient.last_name[0] }}
                    </div>
                </div>
                <h2 class="text-xl font-bold text-slate-900">{{ patient.first_name }} {{ patient.last_name }}</h2>
                <p class="text-sm text-slate-500 mb-4">HN: <span class="font-mono">{{ patient.hn }}</span></p>
                
                <div class="w-full grid grid-cols-2 gap-4 py-4 border-t border-slate-100">
                    <div>
                        <div class="text-xs text-slate-400 uppercase font-bold">Age</div>
                        <div class="font-semibold text-slate-800">28</div>
                    </div>
                    <div>
                        <div class="text-xs text-slate-400 uppercase font-bold">Gender</div>
                        <div class="font-semibold text-slate-800">Female</div>
                    </div>
                    <div class="col-span-2">
                         <div class="text-xs text-slate-400 uppercase font-bold mb-1">Phone</div>
                        <div class="font-semibold text-slate-800">{{ patient.phone_number }}</div>
                    </div>
                </div>

                <div class="w-full mt-4 p-3 bg-red-50 border border-red-100 rounded-xl flex items-start gap-3 text-left">
                    <span class="text-lg">⚠️</span>
                    <div>
                        <div class="text-xs font-bold text-red-800 uppercase">Allergies</div>
                        <div class="text-sm text-red-600 font-medium">Penicillin, Latex</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Vitals Card (Mini) -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 flex-1">
            <h3 class="font-bold text-slate-800 mb-6">Latest Vitals</h3>
            <div class="space-y-4">
                <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100/50">
                    <div class="flex items-center gap-3">
                        <span class="text-xl">❤️</span>
                        <span class="text-sm font-medium text-slate-600">Pulse</span>
                    </div>
                    <span class="font-bold text-slate-900">72 bpm</span>
                </div>
                 <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100/50">
                    <div class="flex items-center gap-3">
                        <span class="text-xl">🩺</span>
                        <span class="text-sm font-medium text-slate-600">Blood Pressure</span>
                    </div>
                    <span class="font-bold text-slate-900">118/75</span>
                </div>
                 <div class="flex items-center justify-between p-4 bg-slate-50 rounded-xl border border-slate-100/50">
                    <div class="flex items-center gap-3">
                        <span class="text-xl">🌡️</span>
                        <span class="text-sm font-medium text-slate-600">Temp</span>
                    </div>
                    <span class="font-bold text-slate-900">36.6°C</span>
                </div>
            </div>
        </div>
    </aside>

    <!-- Main Content Area -->
    <main class="flex-1 flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden min-h-[500px]">
        <!-- Tabs Header -->
        <div class="h-16 border-b border-slate-100 flex items-center justify-between px-4 bg-slate-50/50">
            <div class="flex items-center overflow-x-auto no-scrollbar flex-1 gap-2 pr-4">
                <button 
                    v-for="tab in tabs" 
                    :key="tab.id"
                    @click="activeTab = tab.id"
                    class="h-10 px-4 lg:px-6 rounded-lg text-sm font-medium transition-all flex-shrink-0 flex items-center gap-2 whitespace-nowrap"
                    :class="activeTab === tab.id ? 'bg-white text-brand-600 shadow-sm ring-1 ring-slate-200' : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'"
                >
                    <span>{{ tab.icon }}</span>
                    {{ tab.label }}
                </button>
            </div>
            
            <div class="flex-shrink-0 pl-2 border-l border-slate-200/60">
                <button 
                    class="px-4 py-2 rounded-lg text-sm font-bold shadow-lg transition-all transform hover:-translate-y-0.5 flex items-center gap-2"
                    style="background-color: #ea580c; color: white;"
                >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                    <span class="hidden lg:inline">Start Consultation</span>
                </button>
            </div>
        </div>

        <!-- Tab Content -->
        <div class="flex-1 overflow-y-auto p-4 lg:p-6 bg-slate-50/30">
            <!-- Face Chart Tab -->
            <div v-if="activeTab === 'face-chart'" class="h-full flex flex-col">
                 <FaceCanvas :patientId="patient?.id" />
            </div>

            <!-- Overview Tab Mock -->
            <div v-else-if="activeTab === 'overview'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
                    <h4 class="font-bold text-slate-800 mb-4">Upcoming Appointments</h4>
                    <div class="p-4 bg-brand-50 rounded-lg border border-brand-100 text-brand-700 text-sm font-medium">
                        Nov 24, 2025 - 10:00 AM (Laser Toning)
                    </div>
                </div>
                 <div class="bg-white p-6 rounded-xl border border-slate-100 shadow-sm">
                    <h4 class="font-bold text-slate-800 mb-4">Treatment Plan</h4>
                    <ul class="space-y-2 text-sm text-slate-600 list-disc list-inside">
                        <li>Botox Forehead (Repeat in 3 mos)</li>
                        <li>Acne Clearance (Weekly)</li>
                    </ul>
                </div>
            </div>

            <!-- History Tab -->
            <div v-else-if="activeTab === 'history'" class="space-y-4">
                <div v-if="sessionsLoading" class="text-center py-8 text-slate-500">Loading history...</div>
                <div v-else-if="sessions.length === 0" class="text-center py-8 text-slate-500">No history found.</div>
                <div v-for="session in sessions" :key="session.id" class="bg-white p-4 rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all">
                    <div class="flex justify-between items-start mb-2">
                        <h4 class="font-bold text-slate-800">Session {{ new Date(session.date).toLocaleDateString() }}</h4>
                        <span class="text-xs bg-slate-100 text-slate-500 px-2 py-1 rounded-full">{{ new Date(session.date).toLocaleTimeString() }}</span>
                    </div>
                    <p class="text-sm text-slate-600 mb-3">{{ session.diagnosis_notes || 'No notes recorded.' }}</p>
                    
                    <div v-if="session.images && session.images.length > 0" class="flex gap-2 mt-2">
                        <span class="text-xs font-medium text-brand-600 bg-brand-50 px-2 py-1 rounded-md">
                            📷 {{ session.images.length }} Images Attached
                        </span>
                    </div>
                </div>
            </div>

            <!-- Empty States for others -->
             <div v-else class="h-full flex items-center justify-center text-slate-400 flex-col gap-4 py-12">
                <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center text-2xl">🚧</div>
                <p>This module is under construction</p>
             </div>
        </div>
    </main>
  </div>
</template>
