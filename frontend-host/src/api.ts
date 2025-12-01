import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1/',
    headers: {
        'Content-Type': 'application/json'
    }
})

// Add auth interceptor if we implement login later
// api.interceptors.request.use(...)

export default api

