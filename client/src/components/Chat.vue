<script setup>
import { ref } from 'vue'

const isChatStarted = ref(false)

const messages = ref([{'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}, {'role': 'user', 'content': 'hello'}, {'role': 'assistant', 'content': 'world xxxxxxxxxxxxxxxxxxxxxxsxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}])

let sessionId = null;

async function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const formData = new FormData()
  formData.append('file', file)

  try {
    isSending.value = true
    const res = await fetch('/tutor/start', {
      method: 'POST',
      body: formData
    })
    
    const data = await res.json()
    sessionId = data.id;
    messages.value.push({ 'role': 'assistant', 'content': data.content })
    isChatStarted = true
  } catch (error) {
    console.error('上传失败：', error)
  } finally {
    isSending.value = false
  }
}

const inputMessage = ref('')

const isSending = ref(false)

async function onSend() {
  if (isSending.value) return
  if (!inputMessage.value.trim()) return
  if (!sessionId) return

  const user_text = inputMessage.value.trim()
  messages.value.push({ 'role': 'user', 'content': user_text })
  inputMessage.value = '' 

  try {
    isSending.value = true
    const res = await fetch('/tutor/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'session_id': sessionId, 'user_text': user_text })
    })

    const data = await res.json()
    sessionId = data.id;
    messages.value.push({ 'role': 'assistant', 'content': data.content })
  } catch (error) {
    console.error('上传失败：', error)
  } finally {
    isSending.value = false
  }
}
</script>

<template>
  <div class="chat" v-if="isChatStarted">
    <div class="chat-body">
      <div v-for="msg in messages" :class="msg.role === 'user' ? 'message right' : 'message left'">
        <div class="bubble">{{ msg.content }}</div>
      </div>
      <div v-if="isSending" class="message left">
        <div class="bubble">正在回复中</div>
      </div>
    </div>
    <div class="chat-footer">
      <textarea class="chat-input" placeholder="输入消息..." v-model="inputMessage" @keydown.enter.prevent="onSend"></textarea>
      <button class="chat-send" @click="onSend" aria-label="发送">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2.5"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 19V5" />
          <path d="M5 12l7-7 7 7" />
        </svg>
      </button>
    </div>
  </div>
  <div v-else>
    <p class="chat-welcome">拍照以开始</p>
    <input type="file" accept="image/*" @change="onFileSelect">
  </div>
  
</template>
