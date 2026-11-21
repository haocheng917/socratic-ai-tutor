<script setup>

import { onMounted, ref } from 'vue'
import ErrorNotice from './ErrorNotice.vue'
import { readError, toErrorMessage } from '../utils/http'
import { useChatStore } from '../stores/chat.js'

const baseUrl = import.meta.env.VITE_API_BASE_URL
const isOpen = defineModel()
const sessions = defineModel('sessions')
const props = defineProps(['token'])
const chat = useChatStore()

function selectSession(id) {
  chat.selectSession(id)
  if (window.innerWidth <= 900) {
    isOpen.value = false
  }
}

const isLoading = ref(true)
const loadError = ref('')

async function loadSessions() {
  isLoading.value = true
  loadError.value = ''
  try {
    const res = await fetch(`${baseUrl}/tutor/sessions`, {
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.token}`
      },
    })
    if (!res.ok) {
      throw new Error(await readError(res, '加载对话列表失败'))
    }
    const data = await res.json()
    sessions.value = Array.isArray(data?.sessions) ? data.sessions : []
  } catch (err) {
    console.error(err)
    loadError.value = toErrorMessage(err, '加载对话列表失败')
  } finally {
    isLoading.value = false
  }
}

onMounted(loadSessions)
</script>

<template>
  <aside id="app-sidebar" class="drawer-box" :class="{ open: isOpen }" aria-label="对话记录">
    <div class="drawer-content">
      <header class="drawer-header">
        <div class="drawer-brand">
          <span class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H8l-4 3V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z" />
              <path d="M8 9h8M8 12.5h5" />
            </svg>
          </span>
          <div class="brand-copy">
            <strong>启问</strong>
          </div>
        </div>
        <button class="close-btn" type="button" aria-label="收起侧栏" @click="isOpen = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="m15 18-6-6 6-6"></path>
          </svg>
        </button>
      </header>

      <div class="drawer-section-head">
        <span>历史对话</span>
        <span v-if="sessions && sessions.length" class="history-count">{{ sessions.length }}</span>
      </div>

      <div class="history-list">
        <template v-if="isLoading">
          <div v-for="n in 4" :key="n" class="history-skeleton" aria-hidden="true"></div>
        </template>

        <div v-else-if="loadError" class="history-error">
          <ErrorNotice title="没能加载对话记录" :message="loadError" @dismiss="loadError = ''" />
          <button class="retry-btn" type="button" @click="loadSessions">再试一次</button>
        </div>

        <p v-else-if="!sessions || !sessions.length" class="history-empty">
          还没有对话。点击「新对话」，上传题目照片开始。
        </p>

        <template v-else>
          <button v-for="session in sessions" :key="session.id" type="button" class="history-item"
            :class="{ active: chat.currentSessionId === session.id }"
            :title="session.title || '未命名对话'" @click="selectSession(session.id)">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H8l-4 3V5a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z" />
            </svg>
            <span class="history-title">{{ session.title || '未命名对话' }}</span>
          </button>
        </template>
      </div>
    </div>
  </aside>
</template>
