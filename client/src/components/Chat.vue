<script setup>
import { ref } from 'vue'
import { renderMarkdown } from '../utils/markdown' 

const baseUrl = import.meta.env.VITE_API_BASE_URL

const isChatStarted = ref(false)

const messages = ref([])

let sessionId = null;

async function upload(file) {
  const formData = new FormData()
  formData.append('file', file)
  console.log('正在上传')
  try {
    const res = await fetch(`${baseUrl}/upload`, {
      method: 'POST',
      body: formData
    })
    return await res.json()
  } catch (error) {
    console.error('上传失败：', error)
    throw new Error('上传失败：', error)
  }
}

async function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  isChatStarted.value = true

  isSending.value = true
  const img = await upload(file)

  messages.value.push({
    'role': 'user', 'content': [
      {
        "type": "image_url",
        "image_url": { "url": img.url },
      }
    ]
  })

  try {
    const res = await fetch(`${baseUrl}/tutor/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'content': [
          {
            "type": "image_url",
            "image_url": {"url": img.key},
          }
        ]
      })
    })
    
    const data = await res.json()
    sessionId = data.id;
    messages.value.push({ 'role': 'assistant', 'content': data.content })
  } catch (error) {
    console.error(error)
    messages.value = []
    isChatStarted.value = false
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
    const res = await fetch(`${baseUrl}/tutor/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'session_id': sessionId, 'content': user_text })
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
        <div class="bubble">
          <div v-if="typeof msg.content === 'string'" class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
          <template v-else-if="Array.isArray(msg.content)">
            <template v-for="item in msg.content">
              <img v-if="item.type==='image_url'" :src="item.image_url.url" alt="图片" class="image" />
            </template>
          </template>
        </div>
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
