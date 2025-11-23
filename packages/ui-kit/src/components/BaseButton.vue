<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
}>()
</script>

<template>
  <button
    :class="[
      'px-4 py-2 rounded font-medium transition duration-200',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      variant === 'secondary' 
        ? 'bg-white text-slate-700 border border-slate-300 hover:bg-slate-50' 
        : variant === 'danger'
        ? 'bg-red-600 text-white hover:bg-red-700'
        : 'bg-teal-600 text-white hover:bg-teal-700'
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

