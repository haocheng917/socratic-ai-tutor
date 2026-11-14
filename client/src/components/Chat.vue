<script setup>
import { ref } from 'vue'
import { renderMarkdown } from '../utils/markdown' 

const baseUrl = import.meta.env.VITE_API_BASE_URL

const isChatStarted = ref(false)

const messages = ref([])

let sessionId = null;

async function onFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  
  const formData = new FormData()
  formData.append('file', file)
  isChatStarted.value = true
  console.log('正在上传')

  try {
    isSending.value = true

    sessionId = 1
    messages.value.push({ 'role': 'assistant', 'content': `你好！很高兴和你一起探讨这道几何题。这是一个非常经典的旋转与最短路径结合的问题，里面有很巧妙的转化。\n\n我们一句一句来分析题目，老师先给你留第一个小问题，你思考一下：\n\n**已知条件里说，\\(\\triangle ABC\\) 是等边三角形，\\(BD\\) 是高。**\n根据等边三角形“三线合一”的性质，你能得出高 \\(BD\\) 对边 \\(AC\\) 有什么特殊的几何意义吗？点 \\(E\\) 在 \\(BD\\) 上，这就意味着线段 \\(AE\\) 和 \\(CE\\) 有什么关系？\n\n（你先想一想，告诉我你的发现，我们一步一步往深处走。）` })
    return

    const res = await fetch(`${baseUrl}/tutor/start`, {
      method: 'POST',
      body: formData
    })
    
    const data = await res.json()
    sessionId = data.id;
    messages.value.push({ 'role': 'assistant', 'content': data.content })
  } catch (error) {
    console.error('上传失败：', error)
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
    messages.value.push({ 'role': 'assistant', 'content': `你好！很高兴和你一起探讨这道几何题。这是一个非常经典的旋转与最短路径结合的问题，里面有很巧妙的转化。\n\n我们一句一句来分析题目，老师先给你留第一个小问题，你思考一下：\n\n**已知条件里说，\\(\\triangle ABC\\) 是等边三角形，\\(BD\\) 是高。**\n根据等边三角形“三线合一”的性质，你能得出高 \\(BD\\) 对边 \\(AC\\) 有什么特殊的几何意义吗？点 \\(E\\) 在 \\(BD\\) 上，这就意味着线段 \\(AE\\) 和 \\(CE\\) 有什么关系？\n\n（你先想一想，告诉我你的发现，我们一步一步往深处走。）` })
    return
    const res = await fetch(`${baseUrl}/tutor/chat`, {
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
        <div 
          class="bubble markdown-body" 
          v-html="renderMarkdown(msg.content)"
        ></div>
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
