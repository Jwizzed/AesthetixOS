<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 text-white flex flex-col">
      <div class="p-6 text-xl font-bold tracking-wider border-b border-slate-700">
        Aesthetix<span class="text-teal-400">OS</span>
      </div>
      
      <nav class="flex-1 p-4 space-y-2">
        <RouterLink to="/" 
          class="block px-4 py-3 rounded hover:bg-slate-700 transition"
          active-class="bg-teal-600 hover:bg-teal-600"
        >
          Dashboard
        </RouterLink>
        
        <RouterLink to="/emr" 
          class="block px-4 py-3 rounded hover:bg-slate-700 transition"
          active-class="bg-teal-600 hover:bg-teal-600"
        >
          Medical Records
        </RouterLink>
        
        <RouterLink to="/pos" 
          class="block px-4 py-3 rounded hover:bg-slate-700 transition"
          active-class="bg-teal-600 hover:bg-teal-600"
        >
          Point of Sale
        </RouterLink>
      </nav>
      
      <div class="p-4 border-t border-slate-700 text-sm text-slate-400">
        Logged in as: <span class="text-white">Dr. Smith</span>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <header class="bg-white shadow-sm h-16 flex items-center px-6">
        <h1 class="text-xl font-semibold text-gray-800">Clinic Overview</h1>
      </header>
      
      <div class="p-8">
        <RouterView />
      </div>
    </main>
  </div>
</template>
