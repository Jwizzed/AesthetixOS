<script setup lang="ts">
import { ref, onMounted } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)
const isDrawing = ref(false)
const ctx = ref<CanvasRenderingContext2D | null>(null)

// We will store strokes here to save later
const strokes = ref<{ x: number; y: number; color: string }[][]>([])
const currentStroke = ref<{ x: number; y: number; color: string }[]>([])

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
  currentStroke.value.push({ x: e.offsetX, y: e.offsetY, color: '#FF0000' })
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

const saveAnnotations = () => {
    // In a real app, we would emit this or call the API
    console.log('Saving JSON:', JSON.stringify(strokes.value))
    alert('Annotations saved to console (simulating API call)')
}

onMounted(() => {
  if (canvasRef.value) {
    ctx.value = canvasRef.value.getContext('2d')
    if (ctx.value) {
        ctx.value.strokeStyle = 'red'
        ctx.value.lineWidth = 2
    }
  }
})
</script>

<template>
  <div class="border rounded bg-slate-100 p-4 flex flex-col items-center gap-4">
    <h3 class="font-bold text-slate-700">Face Charting Canvas</h3>
    
    <div class="relative border-2 border-slate-300 bg-white cursor-crosshair">
        <!-- In production, an <img> would be under this canvas -->
        <canvas 
            ref="canvasRef" 
            width="500" 
            height="500"
            @mousedown="startDrawing"
            @mousemove="draw"
            @mouseup="stopDrawing"
            @mouseleave="stopDrawing"
        ></canvas>
    </div>

    <div class="flex gap-2">
        <button @click="clearCanvas" class="px-4 py-2 bg-gray-200 rounded">Clear</button>
        <button @click="saveAnnotations" class="px-4 py-2 bg-teal-600 text-white rounded">Save Annotations</button>
    </div>
  </div>
</template>

