<script setup lang="ts">
import { ref, computed } from 'vue'

interface Product {
    id: number
    name: string
    price: number
    type: 'SERVICE' | 'DRUG'
}

const products: Product[] = [
    { id: 1, name: 'Botox (50U)', price: 12000, type: 'DRUG' },
    { id: 2, name: 'Laser Toning', price: 3500, type: 'SERVICE' },
    { id: 3, name: 'Filler (1cc)', price: 15000, type: 'DRUG' },
    { id: 4, name: 'Facial Treatment', price: 1500, type: 'SERVICE' },
]

const emit = defineEmits(['addToCart'])

</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
    <div 
        v-for="product in products" 
        :key="product.id"
        @click="emit('addToCart', product)"
        class="p-4 border rounded-lg shadow-sm bg-white hover:shadow-md hover:border-teal-500 cursor-pointer transition"
    >
        <div class="text-xs font-bold uppercase text-slate-400 mb-1">{{ product.type }}</div>
        <div class="font-semibold text-slate-800">{{ product.name }}</div>
        <div class="text-teal-600 font-bold mt-2">฿{{ product.price.toLocaleString() }}</div>
    </div>
  </div>
</template>

