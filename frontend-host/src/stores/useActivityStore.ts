import { defineStore } from 'pinia'
import api from '../api'

interface Activity {
    id: string
    time: string
    patientName: string
    patientId: string
    action: string
    status: string
    statusClass: string
}

export const useActivityStore = defineStore('activity', {
    state: () => ({
        activities: [] as Activity[],
        loading: false,
        error: null as string | null
    }),
    actions: {
        async fetchActivities() {
            this.loading = true
            this.error = null
            try {
                // 1. Fetch Transactions (Commerce)
                const trxRes = await api.get('commerce/transactions/')
                // 2. Fetch Patients (Clinic)
                const patRes = await api.get('clinic/patients/')

                const patientsMap = new Map(patRes.data.map((p: any) => [p.id, `${p.first_name} ${p.last_name}`]))

                const transactionActivities = trxRes.data.map((t: any) => ({
                    id: `trx-${t.id}`,
                    time: new Date(t.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                    patientName: patientsMap.get(t.patient_id) || 'Unknown Patient',
                    patientId: t.patient_id,
                    action: `Paid ${t.amount}`,
                    status: t.status,
                    statusClass: t.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                }))

                this.activities = transactionActivities.reverse().slice(0, 10)
            } catch (err) {
                console.error('Failed to fetch activities:', err)
                this.error = 'Failed to load activities'
                // Fallback mock data if API fails
                this.activities = [
                    { id: '1', time: '09:30 AM', patientName: 'Sarah Johnson', patientId: '#PT-2024-001', action: 'Completed Botox Treatment', status: 'Completed', statusClass: 'bg-green-100 text-green-700' },
                    { id: '2', time: '10:15 AM', patientName: 'Michael Chen', patientId: '#PT-2024-002', action: 'Checked in for Consultation', status: 'In Progress', statusClass: 'bg-blue-100 text-blue-700' },
                    { id: '3', time: '11:00 AM', patientName: 'Emma Davis', patientId: '#PT-2024-003', action: 'Payment Processed', status: 'Success', statusClass: 'bg-green-100 text-green-700' },
                ]
            } finally {
                this.loading = false
            }
        }
    }
})
