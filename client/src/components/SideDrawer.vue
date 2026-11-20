<script setup>

import { onMounted, ref } from 'vue'
import ErrorNotice from './ErrorNotice.vue'
import { readError, toErrorMessage } from '../utils/http'

const baseUrl = import.meta.env.VITE_API_BASE_URL
const isOpen = defineModel()
const sessions = defineModel('sessions')
const props = defineProps(['token'])

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
              <path
                d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.8 9.8 0 0 1-3.2-.6L4 21l1.7-4.5A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" />
              <path d="M9 10.5h6M9 13.5h3.5" />
            </svg>
          </span>
          <div class="brand-copy">
            <strong>AI Tutor</strong>
            <small>苏格拉底式学习</small>
          </div>
        </div>
        <button class="close-btn" type="button" aria-label="收起侧栏" @click="isOpen = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
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
          <ErrorNotice title="无法加载对话" :message="loadError" @dismiss="loadError = ''" />
          <button class="retry-btn" type="button" @click="loadSessions">重新加载</button>
        </div>

        <p v-else-if="!sessions || !sessions.length" class="history-empty">
          还没有对话记录<br />上传一道题目，开始第一次思考吧
        </p>

        <template v-else>
          <div v-for="session in sessions" :key="session.id" class="history-item"
            :title="session.title || '未命名对话'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <span class="history-title">{{ session.title || '未命名对话' }}</span>
          </div>
        </template>
      </div>

      <footer class="drawer-footer">
        <strong>拍照提问，边问边学</strong>
        每次只引导一步，让理解真正发生。
      </footer>
    </div>
  </aside>
</template>
