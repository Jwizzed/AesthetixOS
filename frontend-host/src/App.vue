<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'

const isSidebarOpen = ref(false)
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-slate-600 antialiased overflow-hidden">
    <!-- Mobile Sidebar Overlay -->
    <div 
        v-if="isSidebarOpen" 
        @click="isSidebarOpen = false"
        class="fixed inset-0 bg-slate-900/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
    ></div>

    <!-- Sidebar -->
    <aside 
        :class="[
            'w-72 bg-white border-r border-slate-100 flex flex-col fixed inset-y-0 z-50 transition-transform duration-300 ease-in-out',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
    >
      <!-- Logo Area -->
      <div class="h-20 flex items-center px-8 border-b border-slate-50 justify-between lg:justify-start">
        <div class="flex items-center gap-3 group cursor-pointer">
          <div class="w-10 h-10 bg-gradient-to-tr from-brand-500 to-brand-400 rounded-xl flex items-center justify-center shadow-lg shadow-brand-500/20 group-hover:scale-105 transition-transform duration-300">
            <span class="text-white font-bold text-xl">A</span>
          </div>
          <div class="flex flex-col">
            <span class="text-lg font-bold text-slate-900 leading-none tracking-tight">Aesthetix<span class="text-brand-500">OS</span></span>
            <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mt-1">Clinic Admin</span>
          </div>
        </div>
        <!-- Mobile Close Button -->
        <button @click="isSidebarOpen = false" class="lg:hidden text-slate-400 hover:text-slate-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <!-- Navigation -->
      <nav class="flex-1 p-6 space-y-8 overflow-y-auto custom-scrollbar">
        <!-- Main Group -->
        <div class="space-y-2">
          <div class="px-4 text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Main Menu</div>
          
          <RouterLink to="/" 
            @click="isSidebarOpen = false"
            class="flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-200 group relative overflow-hidden"
            active-class="bg-brand-50 text-brand-600 shadow-sm"
            :class="[
               $route.path === '/' ? '' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
            ]"
          >
            <span class="relative z-10 flex items-center gap-3">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
              Dashboard
            </span>
            <div class="absolute inset-0 bg-brand-50 opacity-0 group-hover:opacity-50 transition-opacity duration-200" v-if="$route.path !== '/'"></div>
          </RouterLink>
        </div>

        <!-- Clinical Group -->
        <div class="space-y-2">
           <div class="px-4 text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Clinical</div>
           
           <RouterLink to="/emr" 
            @click="isSidebarOpen = false"
            class="flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-200 group relative overflow-hidden"
            active-class="bg-brand-50 text-brand-600 shadow-sm"
            :class="[
               $route.path.startsWith('/emr') ? '' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
            ]"
          >
             <span class="relative z-10 flex items-center gap-3">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Medical Records
             </span>
          </RouterLink>
        </div>

        <!-- Finance Group -->
        <div class="space-y-2">
           <div class="px-4 text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Finance</div>
           
           <RouterLink to="/pos" 
            @click="isSidebarOpen = false"
            class="flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all duration-200 group relative overflow-hidden"
            active-class="bg-brand-50 text-brand-600 shadow-sm"
            :class="[
               $route.path.startsWith('/pos') ? '' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'
            ]"
          >
             <span class="relative z-10 flex items-center gap-3">
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
               Point of Sale
             </span>
          </RouterLink>
        </div>
      </nav>
      
      <!-- User Profile -->
      <div class="p-4 border-t border-slate-100 m-2">
        <button class="flex items-center gap-3 p-2 w-full rounded-xl hover:bg-slate-50 transition-colors text-left">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-slate-100 to-slate-200 border-2 border-white shadow-sm flex items-center justify-center text-slate-600 font-bold text-sm">DS</div>
            <div class="flex-1 min-w-0">
                <p class="text-sm font-bold text-slate-800 truncate">Dr. Smith</p>
                <p class="text-xs text-slate-500 truncate">Lead Physician</p>
            </div>
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </button>
      </div>
    </aside>

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col lg:pl-72 min-w-0 h-screen">
        <!-- Top Header -->
        <header class="h-16 lg:h-20 bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-slate-200/60 px-4 lg:px-8 flex items-center justify-between shadow-sm transition-all duration-200">
            <!-- Left: Hamburger + Breadcrumbs -->
            <div class="flex items-center gap-4 lg:gap-6 flex-1">
                <!-- Hamburger -->
                <button @click="isSidebarOpen = true" class="lg:hidden p-2 -ml-2 text-slate-500 hover:bg-slate-100 rounded-lg">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
                </button>

                <div class="flex items-center gap-2 text-sm text-slate-400 font-medium">
                    <span class="hidden sm:inline">Clinic</span>
                    <svg class="hidden sm:block w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                    <span class="text-slate-800">{{ $route.name || 'Overview' }}</span>
                </div>
                
                <div class="hidden md:flex items-center relative max-w-md w-full">
                    <svg class="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    <input type="text" placeholder="Search..." class="w-full pl-10 pr-4 py-2 bg-slate-50 border-none rounded-xl text-sm focus:ring-2 focus:ring-brand-500/20 focus:bg-white transition-all duration-200 placeholder-slate-400">
                </div>
            </div>

            <!-- Right Actions -->
            <div class="flex items-center gap-2 lg:gap-4">
                 <button class="md:hidden p-2 text-slate-500 hover:bg-slate-100 rounded-lg">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </button>

                <button class="w-9 h-9 lg:w-10 lg:h-10 rounded-full bg-white border border-slate-100 flex items-center justify-center text-slate-500 hover:text-brand-600 hover:border-brand-200 transition-all shadow-sm relative">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
                    <span class="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full border border-white"></span>
                </button>
                
                <button class="w-9 h-9 lg:w-10 lg:h-10 rounded-full bg-white border border-slate-100 flex items-center justify-center text-slate-500 hover:text-brand-600 hover:border-brand-200 transition-all shadow-sm">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                </button>
            </div>
        </header>
        
        <!-- Main View -->
        <main class="flex-1 overflow-auto p-4 lg:p-8 scroll-smooth">
             <RouterView />
        </main>
    </div>
  </div>
</template>

<style>
/* Custom Scrollbar for Sidebar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
</style>
