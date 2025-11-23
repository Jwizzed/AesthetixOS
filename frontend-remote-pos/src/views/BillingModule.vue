<script setup lang="ts">
import { ref, computed } from 'vue'
import SmartCourseGrid from '../components/SmartCourseGrid.vue'

interface CartItem {
    id: number
    name: string
    price: number
    qty: number
}

const cart = ref<CartItem[]>([])
const isProcessing = ref(false)
const commissionStatus = ref<'IDLE' | 'CALCULATING' | 'DONE'>('IDLE')

const addToCart = (product: any) => {
    const existing = cart.value.find(i => i.id === product.id)
    if (existing) {
        existing.qty++
    } else {
        cart.value.push({ ...product, qty: 1 })
    }
}

const total = computed(() => {
    return cart.value.reduce((sum, item) => sum + (item.price * item.qty), 0)
})

const checkout = async () => {
    if (cart.value.length === 0) return
    
    isProcessing.value = true
    // Simulate API call to create Transaction
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    isProcessing.value = false
    commissionStatus.value = 'CALCULATING'
    
    // Simulate Async Commission Event
    setTimeout(() => {
        commissionStatus.value = 'DONE'
    }, 2000)
}
</script>

<template>
  <div class="flex h-full gap-6 p-6">
    <!-- Left: Product Grid -->
    <div class="flex-1">
        <h2 class="text-2xl font-bold mb-6 text-slate-800">Catalog</h2>
        <SmartCourseGrid @addToCart="addToCart" />
    </div>

    <!-- Right: Cart & Checkout -->
    <div class="w-96 bg-white border rounded-lg shadow-sm flex flex-col">
        <div class="p-4 border-b font-bold text-lg bg-slate-50">Current Bill</div>
        
        <div class="flex-1 p-4 overflow-y-auto space-y-3">
            <div v-if="cart.length === 0" class="text-center text-slate-400 mt-10">
                Cart is empty
            </div>
            <div v-for="item in cart" :key="item.id" class="flex justify-between items-center">
                <div>
                    <div class="font-medium">{{ item.name }}</div>
                    <div class="text-sm text-slate-500">x{{ item.qty }}</div>
                </div>
                <div class="font-bold">฿{{ (item.price * item.qty).toLocaleString() }}</div>
            </div>
        </div>

        <div class="p-6 bg-slate-50 border-t">
            <div class="flex justify-between text-xl font-bold mb-4">
                <span>Total</span>
                <span class="text-teal-700">฿{{ total.toLocaleString() }}</span>
            </div>
            
            <button 
                @click="checkout"
                :disabled="isProcessing || cart.length === 0"
                class="w-full py-3 bg-teal-600 text-white rounded-lg font-bold hover:bg-teal-700 disabled:opacity-50 transition"
            >
                {{ isProcessing ? 'Processing...' : 'Confirm Payment' }}
            </button>

            <!-- Async Commission Status Indicator -->
            <div v-if="commissionStatus !== 'IDLE'" class="mt-4 text-center text-sm">
                <div v-if="commissionStatus === 'CALCULATING'" class="text-blue-600 animate-pulse">
                    ⚡ Calculating Therapist Commissions...
                </div>
                <div v-else class="text-green-600 font-medium">
                    ✓ Commissions Logged
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

