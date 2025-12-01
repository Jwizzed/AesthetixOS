<template>
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
</template>

<script setup lang="ts">
// No props or logic needed for this static component yet
</script>
