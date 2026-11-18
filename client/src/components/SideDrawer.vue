<script setup>

import { onMounted } from 'vue'

const baseUrl = import.meta.env.VITE_API_BASE_URL
const isOpen = defineModel() 
const sessions = defineModel('sessions')
const props = defineProps(['token'])


onMounted(async () => {
  try {
    const res = await fetch(`${baseUrl}/tutor/sessions`, {
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${props.token}`
      },
    })
    const data = await response.json()
    sessions.value = data.sessions
  } catch (err) {
    console.error(err)
  }
})
</script>

<template>
  <div class="drawer-box" :class="{ open: isOpen }">
    <div class="drawer-content">
      <header class="drawer-header">
        <h3 class="project-name">AI Tutor</h3>
        <button class="close-btn" @click="isOpen = false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
        </button>
      </header>
      <div class="history-list">
        <div class="history-item" v-for="id, title in sessions">
          {{ title }}
        </div>
      </div>
    </div>
  </div>
</template>