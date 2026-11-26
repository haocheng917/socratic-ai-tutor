<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { renderMarkdown } from '../utils/markdown'
import { useChatStore } from '../stores/chat'
import { readError, toErrorMessage } from '../utils/http'
import { streamChat } from '../utils/chatStream'
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

// 新建对话时选择教学方式，只有第一次 /tutor/start 会用到
const tutorModes = [
  { value: 'socratic', label: '苏格拉底式', hint: '用提问一步步引导你思考，不急着给答案。' },
  { value: 'direct', label: '直接讲解', hint: '直接讲清知识点和解题步骤，随时可以追问。' },
]
const tutorMode = ref('socratic')
const activeMode = computed(
  () => tutorModes.find((mode) => mode.value === tutorMode.value) || tutorModes[0],
)
const guideSteps = computed(() => (
  tutorMode.value === 'direct'
    ? ['上传题目照片', '我直接讲解思路', '你随时追问细节']
    : ['上传题目照片', '我先问你一个问题', '你在下方回答，我继续追问']
))

// 单选滑块支持左右方向键切换，和原生 radio 的行为保持一致
function onModeKeydown(event) {
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
  event.preventDefault()
  const current = tutorModes.findIndex((mode) => mode.value === tutorMode.value)
  const next = (current + (event.key === 'ArrowRight' ? 1 : -1) + tutorModes.length) % tutorModes.length
  tutorMode.value = tutorModes[next].value
  event.currentTarget
    .closest('.mode-switch')
    ?.querySelectorAll('.mode-option')[next]
    ?.focus()
}

// 流式回复：streamText 是正在接收的内容，streamingConversationId 标记它属于哪个会话
const streamText = ref('')
const streamingConversationId = ref(null)

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

// 只有回复所属会话仍是当前会话时才展示流式内容，
// 避免用户中途切换会话后旧回复串到新会话里
const streamingText = computed(() => (
  streamingConversationId.value !== null
  && streamingConversationId.value === chat.currentConversationId
    ? streamText.value
    : ''
))

// 已发出请求、但还没收到第一个 token 时，才显示“正在想下一步…”
const isWaitingReply = computed(() => (
  isSending.value
  && streamingConversationId.value === chat.currentConversationId
  && !streamingText.value
))

function updateConversationTitle(conversationId, nextTitle) {
  if (!nextTitle) return

  if (Array.isArray(appConversations.value)) {
    const target = appConversations.value.find((item) => item.id === conversationId)
    if (target) {
      target.title = nextTitle
    } else {
      appConversations.value.push({ id: conversationId, title: nextTitle })
    }
  }

  if (chat.currentConversationId === conversationId) {
    chat.title = nextTitle
  }
}

// 调用 /tutor/chat，按 SSE 事件增量更新界面。
// content 可以是纯文本，也可以是 OpenAI 多模态数组（图片）
async function requestChat(conversationId, content) {
  streamingConversationId.value = conversationId
  streamText.value = ''

  try {
    await streamChat({
      baseUrl,
      token: props.token,
      conversationId,
      content,
      onContent(chunk) {
        streamText.value += chunk
      },
      onTitle(nextTitle) {
        updateConversationTitle(conversationId, nextTitle)
      },
    })

    // 流结束后后端已把这一轮写入数据库，本地同步落一条完整消息
    if (streamText.value && chat.currentConversationId === conversationId) {
      chat.messages.push({ role: 'assistant', content: streamText.value })
    }
  } catch (error) {
    // 流中断时保留已收到的部分内容，避免已显示的内容突然消失
    if (streamText.value && chat.currentConversationId === conversationId) {
      chat.messages.push({ role: 'assistant', content: streamText.value })
    }
    throw error
  } finally {
    streamText.value = ''
    streamingConversationId.value = null
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight
    }
  })
}

watch(
  () => [chat.messages.length, isSending.value, streamingText.value],
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

  let conversationId = null

  try {
    const img = await upload(file)

    // 1. 先建一个空会话，并把这次选择的教学方式交给后端
    const startRes = await fetch(`${baseUrl}/tutor/start`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${props.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tutor_mode: tutorMode.value }),
    })

    if (!startRes.ok) {
      throw new Error(await readError(startRes, '获取回复失败'))
    }

    const startData = await startRes.json()
    conversationId = startData.id

    // 2. 本地先展示用户上传的图片（界面用可访问的 url，后端记录 key）
    skipNextLoad = true
    historyError.value = ''
    chat.currentConversationId = conversationId
    chat.messages.push({
      'role': 'user', 'content': [
        {
          "type": "image_url",
          "image_url": { "url": img.url },
        }
      ]
    })
    if (appConversations.value) {
      appConversations.value.push({ 'id': conversationId, 'title': null })
    }

    // 3. 图片作为第一轮用户消息发给 /tutor/chat，流式接收第一次引导
    //    后端按 img.key 存库，读取历史时再换成可访问的 URL
    await requestChat(conversationId, [
      {
        "type": "image_url",
        "image_url": { "url": img.key },
      }
    ])
  } catch (error) {
    console.error(error)
    const message = toErrorMessage(error, '上传失败，请重试')
    if (conversationId === null) {
      // 会话都没建起来，退回上传页展示错误
      chat.messages = []
      uploadError.value = message
    } else {
      // 会话已创建，留在对话页用输入框上方的错误条提示
      sendError.value = message
    }
  } finally {
    isSending.value = false
  }
}

async function onSend() {
  if (isSending.value || isLoadingHistory.value) return
  if (!inputMessage.value.trim()) return
  if (!chat.currentConversationId) return

  const conversationId = chat.currentConversationId
  const userText = inputMessage.value.trim()

  chat.messages.push({ 'role': 'user', 'content': userText })
  inputMessage.value = ''
  sendError.value = ''
  nextTick(() => {
    resizeInput()
  })

  isSending.value = true
  try {
    await requestChat(conversationId, userText)
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

        <!-- 流式回复：边接收边渲染 -->
        <div v-if="streamingText" class="message left">
          <div class="avatar" aria-hidden="true">问</div>
          <div class="bubble">
            <div class="markdown-body" v-html="renderMarkdown(streamingText)"></div>
          </div>
        </div>

        <div v-if="isWaitingReply" class="message left" role="status" aria-label="正在回复">
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

      <div class="mode-picker">
        <span class="mode-picker-label">教学方式</span>
        <div class="mode-switch" role="radiogroup" aria-label="选择教学方式">
          <span class="mode-switch-thumb" :class="`is-${tutorMode}`" aria-hidden="true"></span>
          <button v-for="mode in tutorModes" :key="mode.value" class="mode-option"
            :class="{ active: tutorMode === mode.value }" type="button" role="radio"
            :aria-checked="tutorMode === mode.value" :tabindex="tutorMode === mode.value ? 0 : -1"
            :disabled="isSending" @click="tutorMode = mode.value" @keydown="onModeKeydown">
            {{ mode.label }}
          </button>
        </div>
        <p class="mode-hint">{{ activeMode.hint }}</p>
      </div>

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
          <li v-for="(step, index) in guideSteps" :key="step" class="guide-item">
            <span class="guide-num">{{ index + 1 }}</span>
            <span class="guide-copy">{{ step }}</span>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>
