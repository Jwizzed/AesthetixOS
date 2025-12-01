<template>
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
</template>

<script setup lang="ts">
// Static component
</script>
