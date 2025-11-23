<script setup lang="ts">
import FaceCanvas from '../components/FaceCanvas.vue'

// This is the main entry point that the Host will import
</script>

<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-4 text-slate-800">Patient Electronic Medical Record</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Patient Info Section -->
        <div class="bg-white p-6 rounded-lg shadow-sm border border-slate-200">
            <h3 class="font-semibold mb-4 border-b pb-2">Patient Details</h3>
            <div class="space-y-3">
                <div><span class="text-slate-500">Name:</span> Jane Doe</div>
                <div><span class="text-slate-500">HN:</span> 66-00123</div>
                <div><span class="text-slate-500">Age:</span> 28</div>
                <div class="bg-yellow-50 text-yellow-700 p-2 rounded text-sm mt-4">
                    Allergy Warning: Penicillin
                </div>
            </div>
        </div>

        <!-- Charting Section -->
        <div>
            <FaceCanvas />
        </div>
    </div>
  </div>
</template>

