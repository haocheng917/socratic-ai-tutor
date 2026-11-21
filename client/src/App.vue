<script setup>
import Chat from './components/Chat.vue'
import SideDrawer from './components/SideDrawer.vue'
import AuthPage from './components/AuthPage.vue'
import { ref } from 'vue'
import { useChatStore } from './stores/chat'

const chat = useChatStore()
const token = ref(localStorage.getItem('token') || '')
const isDrawerOpen = ref(window.innerWidth > 900)
const sessions = ref([])
const chatKey = ref(0)

function onLogin(accessToken) {
  token.value = accessToken
  localStorage.setItem('token', accessToken)
}

function startNewChat() {
  chat.currentSessionId = null
  chat.messages = []
  chatKey.value += 1
}

</script>

<template>
  <AuthPage v-if="!token" @login-success="onLogin" />

  <div v-else class="layout-container">
    <SideDrawer v-model="isDrawerOpen" v-model:sessions="sessions" :token="token" />

    <div class="drawer-backdrop" :class="{ visible: isDrawerOpen }" aria-hidden="true"
      @click="isDrawerOpen = false"></div>

    <div class="main-content">
      <header class="top-bar">
        <button class="icon-btn menu-btn" type="button" :aria-expanded="isDrawerOpen" aria-controls="app-sidebar"
          aria-label="切换对话列表" @click="isDrawerOpen = !isDrawerOpen">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 7h16M4 12h16M4 17h10"></path>
          </svg>
        </button>

        <div class="top-bar-title">
          <h1 class="title">启问</h1>
        </div>

        <button class="new-btn" type="button" @click="startNewChat">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M12 5v14M5 12h14"></path>
          </svg>
          <span>新对话</span>
        </button>
      </header>

      <Chat :key="chatKey" :token="token" v-model="sessions" />
    </div>
  </div>
</template>
