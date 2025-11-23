<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary' | 'danger'
  disabled?: boolean
}>()
</script>

<template>
  <button
    :class="[
      'px-4 py-2 rounded-lg font-medium transition-all duration-200 shadow-sm active:scale-95',
      'disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100',
      variant === 'secondary' 
        ? 'bg-white text-brand-600 border border-brand-200 hover:bg-brand-50 hover:border-brand-300' 
        : variant === 'danger'
        ? 'bg-red-500 text-white hover:bg-red-600 shadow-red-100'
        : 'bg-brand-500 text-white hover:bg-brand-600 shadow-brand-200 hover:shadow-brand-300'
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>
