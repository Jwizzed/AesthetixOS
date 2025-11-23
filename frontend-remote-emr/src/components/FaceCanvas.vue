<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{
    patientId?: string
}>()

// --- Setup API ---
const api = axios.create({ baseURL: 'http://localhost:8000/api/v1/clinic/' })

const canvasRef = ref<HTMLCanvasElement | null>(null)
const isDrawing = ref(false)
const ctx = ref<CanvasRenderingContext2D | null>(null)
const isSaving = ref(false)

// Upload State
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedImage = ref<File | null>(null)
const backgroundImageUrl = ref<string | null>(null)

// We will store strokes here to save later
const strokes = ref<{ x: number; y: number; color: string }[][]>([])
const currentStroke = ref<{ x: number; y: number; color: string }[]>([])

const triggerFileInput = () => {
    fileInput.value?.click()
}

const handleImageUpload = (event: Event) => {
    const target = event.target as HTMLInputElement
    if (target.files && target.files[0]) {
        const file = target.files[0]
        uploadedImage.value = file
        // Create local preview URL
        backgroundImageUrl.value = URL.createObjectURL(file)
    }
}

const startDrawing = (e: MouseEvent) => {
  isDrawing.value = true
  if (!ctx.value) return
  
  ctx.value.beginPath()
  ctx.value.moveTo(e.offsetX, e.offsetY)
  
  currentStroke.value = [] // Reset current stroke
}

const draw = (e: MouseEvent) => {
  if (!isDrawing.value || !ctx.value) return
  
  ctx.value.lineTo(e.offsetX, e.offsetY)
  ctx.value.stroke()
  
  // Record point
  currentStroke.value.push({ x: e.offsetX, y: e.offsetY, color: '#EA580C' })
}

const stopDrawing = () => {
  if (isDrawing.value) {
    strokes.value.push([...currentStroke.value])
  }
  isDrawing.value = false
  ctx.value?.closePath()
}

const clearCanvas = () => {
  if (!ctx.value || !canvasRef.value) return
  ctx.value.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)
  strokes.value = []
}

const clearAll = () => {
    clearCanvas()
    uploadedImage.value = null
    backgroundImageUrl.value = null
    if (fileInput.value) fileInput.value.value = ''
}

defineExpose({
    clearAll
})

const saveAnnotations = async () => {
    if (!props.patientId) {
        alert('No patient selected to save session for.')
        return
    }

    isSaving.value = true
    try {
        // 1. Create a new Treatment Session
        const payload = {
            patient: props.patientId,
            diagnosis_notes: "Auto-generated from Face Canvas",
            face_chart_data: strokes.value,
            doctor: 1 // Hardcoded Doctor ID for MVP
        }
        
        console.log('Saving session with payload:', payload)

        const sessionRes = await api.post('sessions/', payload)
        const sessionId = sessionRes.data.id
        console.log('Session created:', sessionId)
        
        // 2. If image exists, upload it
        if (uploadedImage.value) {
            const ext = uploadedImage.value.name.split('.').pop() || 'jpg'
            const contentType = uploadedImage.value.type
            
            // Get Token
            const tokenRes = await api.get(`upload-token/?ext=${ext}&content_type=${encodeURIComponent(contentType)}`)
            const { upload_url, key } = tokenRes.data
            
            // Upload to S3 (Directly)
            await axios.put(upload_url, uploadedImage.value, {
                headers: { 'Content-Type': uploadedImage.value.type }
            })
            
            // Confirm Upload
            await api.post('confirm-upload/', {
                session_id: sessionId,
                key: key,
                image_type: 'BEFORE'
            })
            console.log('Image uploaded and linked')
        }
        
        alert('Session & Face Chart saved successfully!')
        clearAll()

    } catch (error) {
        console.error('Failed to save session:', error)
        alert('Error saving session. Check console.')
    } finally {
        isSaving.value = false
    }
}

onMounted(() => {
  if (canvasRef.value) {
    ctx.value = canvasRef.value.getContext('2d')
    if (ctx.value) {
        ctx.value.strokeStyle = '#ea580c' // Brand-600
        ctx.value.lineWidth = 3
        ctx.value.lineCap = 'round'
        ctx.value.lineJoin = 'round'
    }
  }
})
</script>

<template>
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col h-full">
    <div class="flex items-center justify-between mb-6">
        <h3 class="font-bold text-xl text-slate-900">Face Charting Canvas</h3>
        <div class="flex items-center gap-3">
            <button @click="triggerFileInput" class="text-sm text-brand-600 hover:text-brand-700 font-bold flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {{ uploadedImage ? 'Change Photo' : 'Upload Photo' }}
            </button>
            <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="handleImageUpload" />
            <div class="text-sm text-slate-500">Draw annotations directly on the face chart</div>
        </div>
    </div>
    
    <div class="relative flex-1 min-h-[500px] bg-gray-50 rounded-xl border-2 border-dashed border-gray-200 flex items-center justify-center overflow-hidden group hover:border-brand-300 transition-colors">
        <!-- Background Image or Placeholder -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
             <img v-if="backgroundImageUrl" :src="backgroundImageUrl" class="w-full h-full object-contain opacity-80" />
             <div v-else class="opacity-10">
                <svg class="w-64 h-64 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/></svg>
             </div>
        </div>
        <canvas 
            ref="canvasRef" 
            width="500" 
            height="500"
            class="cursor-crosshair relative z-10 touch-none"
            @mousedown="startDrawing"
            @mousemove="draw"
            @mouseup="stopDrawing"
            @mouseleave="stopDrawing"
        ></canvas>
    </div>

    <div class="flex gap-3 mt-6 justify-end">
        <button 
            @click="clearAll" 
            class="px-4 py-2 bg-white text-slate-600 border border-gray-200 hover:bg-gray-50 rounded-lg font-medium transition-colors"
            :disabled="isSaving"
        >
            Clear All
        </button>
        <button 
            @click="saveAnnotations" 
            class="px-4 py-2 bg-brand-600 text-white hover:bg-brand-700 rounded-lg font-medium shadow-sm transition-colors disabled:opacity-50"
            :disabled="isSaving || !patientId"
        >
            {{ isSaving ? 'Saving...' : 'Save Session & Image' }}
        </button>
    </div>
  </div>
</template>
