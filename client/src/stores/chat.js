import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
    const sessions = ref([])
    const currentSessionId = ref(null)
    const messages = ref([])
    const title = ref('启问')

    function selectSession(id, sessionTitle) {
        currentSessionId.value = id
        const target = sessionTitle || sessions.value.find((session) => session.id === id)?.title
        title.value = target || '启问'
    }

    function addSession(session) {
        sessions.value.push(session)
    }

    return {
        sessions,
        currentSessionId,
        messages,
        title,
        selectSession,
        addSession
    }
})