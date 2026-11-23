import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
    const conversations = ref([])
    const currentConversationId = ref(null)
    const messages = ref([])
    const title = ref('启问')

    function selectConversation(id, conversationTitle) {
        currentConversationId.value = id
        const target = conversationTitle || conversations.value.find((conversation) => conversation.id === id)?.title
        title.value = target || '启问'
    }

    function addConversation(conversation) {
        conversations.value.push(conversation)
    }

    return {
        conversations,
        currentConversationId,
        messages,
        title,
        selectConversation,
        addConversation
    }
})