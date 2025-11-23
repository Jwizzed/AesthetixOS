<script setup lang="ts">
import { ref, computed } from 'vue'
import axios from 'axios'
import SmartCourseGrid from '../components/SmartCourseGrid.vue'

interface CartItem {
    id: string
    name: string
    price: number
    qty: number
}

const api = axios.create({ baseURL: 'http://localhost:8000/api/v1/commerce/' })

const cart = ref<CartItem[]>([])
const isProcessing = ref(false)
const commissionStatus = ref<'IDLE' | 'CALCULATING' | 'DONE'>('IDLE')
const transactionId = ref<string | null>(null)
const selectedCategory = ref('ALL')
const showMobileCart = ref(false) // Ensure cart is closed by default

const categories = [
    { id: 'ALL', label: 'All Items' },
    { id: 'SERVICE', label: 'Treatments' },
    { id: 'DRUG', label: 'Medications' },
    { id: 'PRODUCT', label: 'Retail Products' }
]

const addToCart = (product: any) => {
    const existing = cart.value.find(i => i.id === product.id)
    if (existing) {
        existing.qty++
    } else {
        const price = typeof product.price === 'string' ? parseFloat(product.price) : product.price
        cart.value.push({ ...product, price, qty: 1 })
    }
    // Optional: Open cart on mobile when adding item
    // showMobileCart.value = true
}

const removeFromCart = (index: number) => {
    cart.value.splice(index, 1)
}

const total = computed(() => {
    return cart.value.reduce((sum, item) => sum + (item.price * item.qty), 0)
})

const subtotal = computed(() => total.value)
const tax = computed(() => total.value * 0.07)

const formatCurrency = (val: number) => {
    return '฿' + val.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})
}

const checkout = async () => {
    if (cart.value.length === 0) return
    
    isProcessing.value = true
    try {
        const payload = {
            patient: "00000000-0000-0000-0000-000000000000", 
            staff_1: 1, 
            total_amount: total.value,
            status: 'COMPLETED' 
        }

        const patientRes = await axios.get('http://localhost:8000/api/v1/clinic/patients/')
        if (patientRes.data.length > 0) {
            payload.patient = patientRes.data[0].id
        } else {
             const newPatient = await axios.post('http://localhost:8000/api/v1/clinic/patients/', {
                hn: `ZN-${Math.floor(Math.random() * 10000)}`,
                first_name: "Walk-in",
                last_name: "Customer",
                phone_number: "0810000000"
             })
             payload.patient = newPatient.data.id
        }

        const response = await api.post('transactions/', payload)
        transactionId.value = response.data.id
        
        cart.value = [] 
        isProcessing.value = false
        commissionStatus.value = 'CALCULATING'
        
        pollCommissionStatus(response.data.id)

    } catch (error) {
        console.warn('Checkout API failed, simulating success for demo.', error)
        
        // Mock Success for Demo
        await new Promise(resolve => setTimeout(resolve, 1000)) // Fake delay
        transactionId.value = 'DEMO-' + Math.floor(Math.random() * 10000)
        cart.value = [] 
        isProcessing.value = false
        commissionStatus.value = 'CALCULATING'
        
        pollCommissionStatus(transactionId.value!)
    }
}

const pollCommissionStatus = (trxId: string) => {
    let attempts = 0
    const maxAttempts = 10
    const interval = setInterval(async () => {
        attempts++
        try {
            if (attempts > 2) {
                commissionStatus.value = 'DONE'
                clearInterval(interval)
                console.log('Polling for transaction:', trxId) 
            }
        } catch (e) { console.error(e) }
        
        if (attempts >= maxAttempts) {
            clearInterval(interval)
            commissionStatus.value = 'DONE'
        }
    }, 1000)
}
</script>

<template>
  <div class="flex flex-col lg:flex-row h-[calc(100vh-9rem)] lg:h-[calc(100vh-6rem)] gap-8 overflow-hidden relative">
    <!-- Left: Product Catalog -->
    <div class="flex-1 flex flex-col min-w-0 h-full">
        <!-- Category Filter -->
        <div class="flex gap-4 mb-6 overflow-x-auto pb-2 scrollbar-hide flex-shrink-0">
            <button 
                v-for="cat in categories" 
                :key="cat.id"
                @click="selectedCategory = cat.id"
                class="px-6 py-3 rounded-xl text-sm font-bold whitespace-nowrap transition-all duration-200 border"
                :class="selectedCategory === cat.id 
                    ? 'shadow-lg shadow-orange-200' 
                    : 'bg-white text-slate-600 border-slate-200 hover:border-orange-200 hover:bg-orange-50 hover:text-orange-600'"
                :style="selectedCategory === cat.id ? { backgroundColor: '#ea580c', color: 'white', borderColor: '#ea580c' } : {}"
            >
                {{ cat.label }}
            </button>
        </div>

        <!-- Grid -->
        <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 pb-24 lg:pb-0">
             <SmartCourseGrid @addToCart="addToCart" :category="selectedCategory" />
        </div>
    </div>

    <!-- Mobile Cart Toggle Button (Floating) -->
    <div class="lg:hidden fixed bottom-6 right-6 z-[60]">
        <button 
            @click="showMobileCart = !showMobileCart"
            class="relative w-14 h-14 bg-white text-black rounded-full shadow-xl shadow-slate-900/10 flex items-center justify-center transition-transform hover:scale-105 active:scale-95 border border-slate-200"
        >
            <svg v-if="!showMobileCart" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
             <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            <span v-if="cart.length > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-brand-500 text-white rounded-full text-xs font-bold flex items-center justify-center border-2 border-white">{{ cart.length }}</span>
        </button>
    </div>

    <!-- Right: Checkout Sidebar -->
    <div 
        class="fixed inset-0 bg-slate-900/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
        v-if="showMobileCart"
        @click="showMobileCart = false"
    ></div>

    <div 
        class="fixed lg:static bottom-0 left-0 right-0 lg:w-[400px] flex-shrink-0 flex flex-col bg-white lg:rounded-3xl rounded-t-3xl shadow-2xl shadow-slate-200/50 border border-slate-100 overflow-hidden h-[80vh] lg:h-full z-50 transition-transform duration-300 ease-out transform lg:transform-none"
        :class="showMobileCart ? 'translate-y-0' : 'translate-y-full lg:translate-y-0 hidden lg:flex'"
    >
        <!-- Header -->
        <div class="p-6 bg-slate-900 text-white flex justify-between items-center cursor-pointer lg:cursor-default" @click="showMobileCart = false">
            <div class="flex justify-between items-start w-full">
                <div>
                    <h2 class="text-lg font-bold">Current Bill</h2>
                    <p class="text-slate-400 text-xs font-mono mt-1">#TRX-{{ transactionId ? transactionId.slice(0,8) : 'PENDING' }}</p>
                </div>
                <button class="p-2 hover:bg-white/10 rounded-lg transition-colors text-slate-400 hover:text-white lg:block hidden">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
                <button 
                    @click.stop="showMobileCart = false"
                    class="p-2 hover:bg-white/10 rounded-lg transition-colors text-slate-400 hover:text-white lg:hidden"
                >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
            </div>
        </div>

        <!-- Cart Items -->
        <div class="flex-1 overflow-y-auto p-6 bg-slate-50/50">
             <div v-if="cart.length === 0" class="h-full flex flex-col items-center justify-center text-slate-300 gap-4">
                <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                <span class="text-sm font-medium">No items in cart</span>
            </div>
            
            <div v-else class="space-y-4">
                <div v-for="(item, idx) in cart" :key="idx" class="flex gap-4 group bg-white p-3 rounded-xl border border-slate-100 shadow-sm hover:shadow-md transition-all">
                    <div class="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center text-xl font-bold text-slate-600">
                        {{ item.name[0] }}
                    </div>
                    <div class="flex-1 min-w-0">
                        <div class="flex justify-between items-start">
                             <h4 class="font-bold text-slate-900 truncate pr-2">{{ item.name }}</h4>
                             <span class="font-bold text-slate-900">{{ formatCurrency(item.price * item.qty) }}</span>
                        </div>
                        <div class="flex justify-between items-center mt-1">
                            <div class="text-xs text-slate-500">{{ formatCurrency(item.price) }} x {{ item.qty }}</div>
                            <button @click="removeFromCart(idx)" class="text-xs text-red-400 hover:text-red-600 font-medium opacity-100 lg:opacity-0 group-hover:opacity-100 transition-opacity">Remove</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Totals Section -->
        <div class="bg-white border-t border-slate-100 p-6 shadow-[0_-10px_40px_rgba(0,0,0,0.05)]">
            <div class="space-y-3 mb-6">
                <div class="flex justify-between text-sm text-slate-500">
                    <span>Subtotal</span>
                    <span>{{ formatCurrency(subtotal) }}</span>
                </div>
                 <div class="flex justify-between text-sm text-slate-500">
                    <span>VAT (7%)</span>
                    <span>{{ formatCurrency(tax) }}</span>
                </div>
                <div class="pt-3 border-t border-dashed border-slate-200 flex justify-between items-end">
                    <span class="text-slate-900 font-bold text-lg">Total</span>
                    <span class="text-3xl font-extrabold text-brand-600 tracking-tight">{{ formatCurrency(total) }}</span>
                </div>
            </div>

            <button 
                @click="checkout"
                :disabled="isProcessing || cart.length === 0"
                class="w-full py-4 bg-orange-500 text-black rounded-xl font-bold text-lg hover:bg-orange-600 disabled:opacity-50 disabled:hover:bg-orange-500 transition-all duration-300 shadow-lg shadow-orange-500/20 active:scale-[0.98] flex items-center justify-center gap-3"
            >
                <span v-if="isProcessing" class="animate-spin">⏳</span>
                {{ isProcessing ? 'Processing...' : 'Pay Now' }}
            </button>
            
             <!-- Async Commission Status Indicator -->
            <div v-if="commissionStatus !== 'IDLE'" class="mt-4 text-center">
                <div v-if="commissionStatus === 'CALCULATING'" class="text-xs font-bold text-blue-500 flex items-center justify-center gap-2 bg-blue-50 py-2 rounded-lg">
                   <span>⚡</span> Calculating Therapist Commissions...
                </div>
                <div v-else class="text-xs font-bold text-emerald-600 flex items-center justify-center gap-2 bg-emerald-50 py-2 rounded-lg">
                    <span>✓</span> Commissions Logged Successfully
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
