<script setup>
import { ref } from 'vue'
import { renderMarkdown } from '../utils/markdown'
import { useChatStore } from '../stores/chat'

const baseUrl = import.meta.env.VITE_API_BASE_URL

const chat = useChatStore()

const props = defineProps(['token'])

const isSending = ref(false)
const uploadError = ref('')

async function readError(res, prefix) {
  let detail = `HTTP ${res.status}`
  try {
    const data = await res.json()
    if (data && data.detail) {
      detail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
    }
  } catch (e) {
    // 响应不是 JSON，保留状态码信息
  }
  return `${prefix}：${detail}`
}

async function upload(file) {
  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch(`${baseUrl}/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${props.token}`
    },
    body: formData
  })

  if (!res.ok) {
    throw new Error(await readError(res, '上传失败'))
  }

  const data = await res.json()
  if (!data || !data.key || !data.url) {
    throw new Error('上传失败：服务端未返回图片地址')
  }
  return data
}

async function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  event.target.value = ''

  isSending.value = true
  uploadError.value = ''

  try {
    const img = await upload(file)

    chat.messages.value.push({
      'role': 'user', 'content': [
        {
          "type": "image_url",
          "image_url": { "url": img.url },
        }
      ]
    })

    const res = await fetch(`${baseUrl}/tutor/start`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.token}`
      },
      body: JSON.stringify({
        'content': [
          {
            "type": "image_url",
            "image_url": { "url": img.key },
          }
        ]
      })
    })

    if (!res.ok) {
      throw new Error(await readError(res, '获取回复失败'))
    }

    const data = await res.json()
    chat.currentSessionId = data.id;
    chat.messages.value.push({ 'role': 'assistant', 'content': data.content })
    chat.sessions.value.push({ 'title': 'New chat', 'id': chat.currentSessionId })
  } catch (error) {
    console.error(error)
    chat.messages.value = []
    uploadError.value = error.message || '上传失败，请重试'
  } finally {
    isSending.value = false
  }
}

const inputMessage = ref('')

async function onSend() {
  if (isSending.value) return
  if (!inputMessage.value.trim()) return
  if (!currentSessionId) return

  const user_text = inputMessage.value.trim()
  chat.messages.value.push({ 'role': 'user', 'content': user_text })
  inputMessage.value = ''

  try {
    isSending.value = true
    const res = await fetch(`${baseUrl}/tutor/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.token}`
      },
      body: JSON.stringify({ 'session_id': chat.currentSessionId, 'content': user_text })
    })

    if (!res.ok) {
      throw new Error(await readError(res, '发送失败'))
    }

    const data = await res.json()
    chat.currentSessionId = data.id;
    chat.messages.value.push({ 'role': 'assistant', 'content': data.content })
  } catch (error) {
    console.error('发送失败：', error)
  } finally {
    isSending.value = false
  }
}
</script>

<template>
  <div class="chat">
    <template v-if="chat.currentSessionId !== null">
      <div class="chat-body">
        <div v-for="msg in chat.messages" :class="msg.role === 'user' ? 'message right' : 'message left'">
          <div class="bubble">
            <div v-if="typeof msg.content === 'string'" class="markdown-body" v-html="renderMarkdown(msg.content)">
            </div>
            <template v-else-if="Array.isArray(msg.content)">
              <template v-for="item in msg.content">
                <img v-if="item.type === 'image_url'" :src="item.image_url.url" alt="图片" class="image" />
              </template>
            </template>
          </div>
        </div>
        <div v-if="isSending" class="message left">
          <div class="bubble">正在回复中</div>
        </div>
      </div>
      <div class="chat-footer">
        <textarea class="chat-input" placeholder="输入消息..." v-model="inputMessage"
          @keydown.enter.prevent="onSend"></textarea>
        <button class="chat-send" @click="onSend" aria-label="发送">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 19V5" />
            <path d="M5 12l7-7 7 7" />
          </svg>
        </button>
      </div>
    </template>
    <div v-else>
      <div class="chat-welcome">
        <p class="chat-hint">拍照以开始</p>
        <label class="start-btn">
          <input type="file" accept="image/*" :disabled="isSending" @change="onFileSelect">

          上传图片
        </label>
        <p v-if="isSending" class="upload-status">正在上传图片...</p>
        <p v-if="uploadError" class="upload-error">{{ uploadError }}</p>
      </div>
    </div>
  </div>

</template>
