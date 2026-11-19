import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
    const sessions = ref([])
    const currentSessionId = ref(null)
    const messages = ref([])
    const loading = ref(false)

    function selectSession(id) {
        currentSessionId.value = id
    }

    function addSession(session) {
        sessions.value.push(session)
    }

    return {
        sessions,
        currentSessionId,
        messages,
        loading,
        selectSession,
        addSession
    }
})