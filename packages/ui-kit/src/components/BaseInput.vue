<script setup lang="ts">
defineProps<{
  label: string
  modelValue: string | number
  type?: string
  placeholder?: string
}>()

defineEmits(['update:modelValue'])
</script>

<template>
  <div class="flex flex-col gap-1">
    <label class="text-sm font-medium text-slate-700">{{ label }}</label>
    <input
      :type="type || 'text'"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :placeholder="placeholder"
      class="px-3 py-2 border border-slate-300 rounded focus:outline-none focus:ring-2 focus:ring-teal-500"
    />
  </div>
</template>

