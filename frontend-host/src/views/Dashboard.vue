<template>
  <div class="space-y-6 lg:space-y-10">
    <!-- Hero Section -->
    <DashboardHero />
    
    <!-- Key Metrics -->
    <DashboardMetrics />

    <!-- Main Modules Grid -->
    <DashboardModules />

    <!-- Recent Activity Table -->
    <DashboardActivity />
  </div>
</template>

<script setup lang="ts">
import DashboardHero from '../components/dashboard/DashboardHero.vue'
import DashboardMetrics from '../components/dashboard/DashboardMetrics.vue'
import DashboardModules from '../components/dashboard/DashboardModules.vue'
import DashboardActivity from '../components/dashboard/DashboardActivity.vue'
</script>