<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { renderMarkdown } from '../utils/markdown'
import { useChatStore } from '../stores/chat'
import { readError, toErrorMessage } from '../utils/http'
import ErrorNotice from './ErrorNotice.vue'

const baseUrl = import.meta.env.VITE_API_BASE_URL

const chat = useChatStore()

const props = defineProps(['token'])
const appConversations = defineModel()

const isSending = ref(false)
const uploadError = ref('')
const sendError = ref('')
const historyError = ref('')
const showNextStepHint = ref(true)
const isLoadingHistory = ref(false)
const inputMessage = ref('')
const chatBody = ref(null)
const inputEl = ref(null)

// 新建会话时跳过历史加载，切换历史会话时才拉取
let skipNextLoad = false
let historyRequest = 0

async function loadMessage() {
  const conversationId = chat.currentConversationId
  if (!conversationId) {
    chat.messages = []
    return
  }

  const requestId = ++historyRequest
  isLoadingHistory.value = true
  historyError.value = ''

  try {
    const res = await fetch(`${baseUrl}/tutor/history/${conversationId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${props.token}`
      },
    })

    if (!res.ok) {
      throw new Error(await readError(res, '加载对话失败'))
    }

    const data = await res.json()
    if (requestId !== historyRequest) return
    if (!Array.isArray(data?.messages)) {
      throw new Error('加载对话失败：服务端返回格式不正确')
    }

    // 历史中包含 system 提示词，界面只展示用户和助手的消息
    chat.messages = data.messages.filter(
      (message) => message.role === 'user' || message.role === 'assistant',
    )
    scrollToBottom()
  } catch (error) {
    if (requestId !== historyRequest) return
    console.error(error)
    chat.messages = []
    historyError.value = toErrorMessage(error, '加载对话失败，请重试')
  } finally {
    if (requestId === historyRequest) {
      isLoadingHistory.value = false
    }
  }
}

watch(
  () => chat.currentConversationId,
  (newId, oldId) => {
    if (newId === oldId) return

    if (skipNextLoad) {
      skipNextLoad = false
      return
    }

    historyRequest += 1
    isLoadingHistory.value = false
    historyError.value = ''
    chat.messages = []

    if (newId) {
      loadMessage()
    }
  },
)

const hasUserText = computed(() => chat.messages.some(
  (message) => message.role === 'user' && typeof message.content === 'string',
))

function scrollToBottom() {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight
    }
  })
}

watch(
  () => [chat.messages.length, isSending.value],
  () => scrollToBottom(),
)

function resizeInput() {
  const el = inputEl.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 150)}px`
}

watch(inputMessage, () => nextTick(resizeInput))

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
  sendError.value = ''

  try {
    const img = await upload(file)

    chat.messages.push({
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
    skipNextLoad = true
    historyError.value = ''
    chat.currentConversationId = data.id
    chat.messages.push({ 'role': 'assistant', 'content': data.content })
    if (appConversations.value) {
      appConversations.value.push({ 'title': '新对话', 'id': chat.currentConversationId })
    }
  } catch (error) {
    console.error(error)
    chat.messages = []
    uploadError.value = toErrorMessage(error, '上传失败，请重试')
  } finally {
    isSending.value = false
  }
}

async function onSend() {
  if (isSending.value || isLoadingHistory.value) return
  if (!inputMessage.value.trim()) return
  if (!chat.currentConversationId) return

  const conversationId = chat.currentConversationId
  const user_text = inputMessage.value.trim()
  chat.messages.push({ 'role': 'user', 'content': user_text })
  inputMessage.value = ''
  sendError.value = ''
  nextTick(() => {
    resizeInput()
  })

  try {
    isSending.value = true
    const res = await fetch(`${baseUrl}/tutor/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.token}`
      },
      body: JSON.stringify({ 'conversation_id': conversationId, 'content': user_text })
    })

    if (!res.ok) {
      throw new Error(await readError(res, '发送失败'))
    }

    const data = await res.json()
    if (chat.currentConversationId === conversationId) {
      chat.messages.push({ 'role': 'assistant', 'content': data.content })
    }
  } catch (error) {
    console.error('发送失败：', error)
    sendError.value = toErrorMessage(error, '发送失败，请稍后重试')
  } finally {
    isSending.value = false
  }
}

function onEnter(event) {
  // 中文输入法组词时的回车用于确认候选词，不触发发送
  if (event.isComposing || event.keyCode === 229) return
  event.preventDefault()
  onSend()
}
</script>

<template>
  <div class="chat">
    <template v-if="chat.currentConversationId !== null">
      <div ref="chatBody" class="chat-body" aria-live="polite">
        <div v-if="isLoadingHistory" class="history-loading">
          <span class="spinner" aria-hidden="true"></span>
          正在加载对话…
        </div>
        <div v-else-if="historyError" class="history-load-error">
          <ErrorNotice title="没能加载这段对话" :message="historyError" :dismissible="false" />
          <button class="retry-btn history-retry" type="button" @click="loadMessage">再试一次</button>
        </div>
        <div v-for="(msg, index) in chat.messages" :key="index"
          :class="msg.role === 'user' ? 'message right' : 'message left'">
          <div class="avatar" aria-hidden="true">
            {{ msg.role === 'user' ? '我' : '问' }}
          </div>
          <div class="bubble" :class="{ 'has-image': Array.isArray(msg.content) }">
            <div v-if="typeof msg.content === 'string'" class="markdown-body" v-html="renderMarkdown(msg.content)">
            </div>
            <template v-else-if="Array.isArray(msg.content)">
              <template v-for="(item, itemIndex) in msg.content" :key="itemIndex">
                <img v-if="item.type === 'image_url'" :src="item.image_url.url" alt="上传的题目图片" class="image" />
              </template>
            </template>
          </div>
        </div>

        <div v-if="isSending" class="message left" role="status" aria-label="正在回复">
          <div class="avatar" aria-hidden="true">问</div>
          <div class="bubble typing-bubble">
            <span class="typing-dots" aria-hidden="true"><i></i><i></i><i></i></span>
            <span class="typing-label">正在想下一步…</span>
          </div>
        </div>
      </div>

      <div class="chat-composer">
        <div v-if="showNextStepHint && !hasUserText && !isSending && !isLoadingHistory && !historyError"
          class="next-step-hint">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" aria-hidden="true">
            <path d="M9 18l6-6-6-6"></path>
          </svg>
          <span><strong>轮到你了</strong>：在下方写下你的想法，按 Enter 发送。</span>
          <button class="next-step-close" type="button" aria-label="关闭提示" @click="showNextStepHint = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              aria-hidden="true">
              <path d="M6 6l12 12M18 6L6 18"></path>
            </svg>
          </button>
        </div>

        <div v-if="sendError" class="composer-error">
          <ErrorNotice title="消息没发出去" :message="sendError" @dismiss="sendError = ''" />
        </div>

        <div class="chat-footer">
          <textarea ref="inputEl" class="chat-input" rows="1" placeholder="写下你的想法，按 Enter 发送…" v-model="inputMessage"
            aria-label="输入消息" :disabled="isLoadingHistory" @input="resizeInput"
            @keydown.enter.exact="onEnter"></textarea>
          <button class="chat-send" type="button" aria-label="发送消息"
            :disabled="isSending || isLoadingHistory || !inputMessage.trim()" @click="onSend">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 19V5" />
              <path d="M5 12l7-7 7 7" />
            </svg>
          </button>
        </div>

      </div>
    </template>

    <div v-else class="chat-welcome">
      <h1 class="welcome-title">把题目照片传上来</h1>

      <label class="upload-card" :class="{ busy: isSending }">
        <input type="file" accept="image/*" :disabled="isSending" @change="onFileSelect">
        <span class="upload-icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
            stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="3" ry="3"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <path d="m21 15-4.5-4.5L7 20"></path>
          </svg>
        </span>
        <span class="upload-copy">
          <span class="upload-card-title">选择题目照片</span>
        </span>
        <span class="upload-cta" aria-hidden="true">选择图片</span>
      </label>

      <p v-if="isSending" class="upload-status">
        <span class="spinner" aria-hidden="true"></span>
        正在上传，请稍等…
      </p>

      <div v-if="uploadError" class="welcome-error">
        <ErrorNotice title="没能开始对话" :message="uploadError" @dismiss="uploadError = ''" />
      </div>

      <div class="welcome-guide">
        <ol class="guide-list">
          <li class="guide-item"><span class="guide-num">1</span><span class="guide-copy">上传题目照片</span></li>
          <li class="guide-item"><span class="guide-num">2</span><span class="guide-copy">我先问你一个问题</span></li>
          <li class="guide-item"><span class="guide-num">3</span><span class="guide-copy">你在下方回答，我继续追问</span></li>
        </ol>
      </div>
    </div>
  </div>
</template>
