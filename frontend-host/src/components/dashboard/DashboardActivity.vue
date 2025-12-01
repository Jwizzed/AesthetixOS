<template>
    <div class="bg-white rounded-3xl shadow-sm border border-slate-100 overflow-hidden">
        <div class="p-6 border-b border-slate-50 flex justify-between items-center">
            <h3 class="font-bold text-slate-800 text-lg">Recent Transactions</h3>
            <button @click="store.fetchActivities()" class="text-sm text-brand-600 font-medium hover:text-brand-700 flex items-center gap-1">
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
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useActivityStore } from '../../stores/useActivityStore'
import { storeToRefs } from 'pinia'

const store = useActivityStore()
const { activities, loading } = storeToRefs(store)

onMounted(() => {
    store.fetchActivities()
})
</script>
