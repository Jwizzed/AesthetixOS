<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'

interface Product {
    id: string
    name: string
    price: number | string
    type: 'SERVICE' | 'DRUG' | 'PRODUCT'
    product_type?: 'SERVICE' | 'DRUG' | 'RETAIL' // Backend type
    image?: string
}

const props = defineProps<{
    category?: string
}>()

const emit = defineEmits(['addToCart'])

// API Client
const api = axios.create({ baseURL: 'http://localhost:8000/api/v1/commerce/' })

const products = ref<Product[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

const fetchProducts = async () => {
    loading.value = true
    error.value = null
    try {
        const response = await api.get('products/')
        // Map backend data to frontend structure
        products.value = response.data.map((p: any) => ({
            id: p.id,
            name: p.name,
            price: Number(p.price), // Ensure number
            type: p.product_type === 'RETAIL' ? 'PRODUCT' : p.product_type, // Map RETAIL to PRODUCT
            image: undefined
        }))
    } catch (e) {
        console.error('Failed to fetch products', e)
        error.value = 'Failed to load products. using offline backup.'
        // Fallback to hardcoded if API fails (for demo robustness)
        products.value = fallbackProducts
    } finally {
        loading.value = false
    }
}

const fallbackProducts: Product[] = [
    { id: '1', name: 'Botox (50U)', price: 12000, type: 'DRUG' },
    { id: '2', name: 'Laser Toning', price: 3500, type: 'SERVICE' },
    { id: '3', name: 'Filler (1cc)', price: 15000, type: 'DRUG' },
    { id: '4', name: 'Facial Treatment', price: 1500, type: 'SERVICE' },
    { id: '5', name: 'Vitamin Drip', price: 2500, type: 'SERVICE' },
    { id: '6', name: 'Acne Clear Set', price: 800, type: 'PRODUCT' },
    { id: '7', name: 'Sunscreen SPF50', price: 1200, type: 'PRODUCT' },
    { id: '8', name: 'HIFU Full Face', price: 18000, type: 'SERVICE' },
    { id: '9', name: 'Whitening Cream', price: 950, type: 'PRODUCT' },
]

onMounted(() => {
    fetchProducts()
})

const filteredProducts = computed(() => {
    if (!props.category || props.category === 'ALL') {
        return products.value
    }
    return products.value.filter(p => p.type === props.category)
})

const getCategoryColor = (type: string) => {
    switch(type) {
        case 'SERVICE': return 'bg-blue-50 text-blue-600 border-blue-100'
        case 'DRUG': return 'bg-purple-50 text-purple-600 border-purple-100'
        case 'PRODUCT': return 'bg-emerald-50 text-emerald-600 border-emerald-100'
        default: return 'bg-gray-50 text-gray-600'
    }
}
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4">
    <div 
        v-for="product in filteredProducts" 
        :key="product.id"
        @click="emit('addToCart', product)"
        class="group p-5 border border-gray-100 rounded-2xl shadow-sm bg-white hover:shadow-xl hover:shadow-brand-900/5 hover:border-brand-200 cursor-pointer transition-all duration-300 transform hover:-translate-y-1 relative overflow-hidden flex flex-col h-full"
    >
        <!-- Decorative Background -->
        <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-transparent to-slate-50 rounded-bl-[100%] -mr-8 -mt-8 transition-colors group-hover:to-brand-50/50"></div>
        
        <div class="relative z-10 flex-1 flex flex-col gap-4 p-2">
             <div class="flex justify-between items-start mb-4">
                <span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border shadow-sm"
                    :class="getCategoryColor(product.type)"
                >
                    {{ product.type }}
                </span>
             </div>
            
            <div class="font-bold text-slate-900 text-lg mb-6 group-hover:text-brand-600 transition-colors leading-snug min-h-[3.5rem]">
                {{ product.name }}
            </div>
            
            <div class="mt-auto flex items-end justify-between border-t border-dashed border-slate-100 pt-4">
                <div class="text-brand-600 font-bold text-xl flex items-baseline gap-1">
                    <span class="text-sm text-brand-400 font-medium">฿</span>{{ product.price.toLocaleString() }}
                </div>
                
                <div class="w-10 h-10 rounded-xl bg-slate-50 text-slate-400 group-hover:bg-brand-500 group-hover:text-white flex items-center justify-center transition-all shadow-sm hover:shadow-brand-200">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4"></path></svg>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
