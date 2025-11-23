<template>
  <div class="p-6 bg-white rounded-lg shadow-sm">
    <h2 class="text-2xl font-bold text-slate-800 mb-4">Welcome to AesthetixOS</h2>
    <p class="text-slate-600 mb-6">
      Select a module from the sidebar to get started.
    </p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <router-link to="/emr" class="group block p-6 border border-slate-200 rounded-lg hover:border-teal-500 hover:shadow-md transition">
        <h3 class="text-lg font-semibold text-teal-600 group-hover:text-teal-700">Medical Records (EMR)</h3>
        <p class="text-slate-500 mt-2">Manage patient profiles, history, and face charts.</p>
      </router-link>
      
      <router-link to="/pos" class="group block p-6 border border-slate-200 rounded-lg hover:border-teal-500 hover:shadow-md transition">
        <h3 class="text-lg font-semibold text-teal-600 group-hover:text-teal-700">Point of Sale (POS)</h3>
        <p class="text-slate-500 mt-2">Process payments, manage inventory, and billing.</p>
      </router-link>
    </div>
  </div>
</template>

