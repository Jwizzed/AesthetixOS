<template>
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
</template>

<script setup lang="ts">
const stats = [
    { label: 'Total Revenue', value: '฿124,500', icon: '💰', bgClass: 'bg-green-50 text-green-600', trend: 12.5 },
    { label: 'Appointments', value: '48', icon: '📅', bgClass: 'bg-blue-50 text-blue-600', trend: 8.2 },
    { label: 'New Patients', value: '15', icon: '👥', bgClass: 'bg-purple-50 text-purple-600', trend: -2.4 },
    { label: 'Inventory Alerts', value: '3', icon: '⚠️', bgClass: 'bg-orange-50 text-orange-600', trend: 0 },
]
</script>
