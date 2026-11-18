<script setup>
import Chat from './components/Chat.vue'
import SideDrawer from './components/SideDrawer.vue'
import AuthPage from './components/AuthPage.vue'
import { ref } from 'vue'

const token = ref(localStorage.getItem('token') || '')
const isDrawerOpen = ref(true)

function onLogin(accessToken) {
  token.value = accessToken
  localStorage.setItem('token', accessToken)
}

</script>

<template>
  <AuthPage v-if="!token" @login-success="onLogin" />

  <div v-else class="layout-container">
    <SideDrawer v-model="isDrawerOpen" />
    <div class="main-content">
      <header class="top-bar">
        <button v-if="!isDrawerOpen" class="open-btn" @click="isDrawerOpen = !isDrawerOpen">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
        </button>
        <h3 class="title">Chat Title</h3>
        <button class="new-btn" @click="startNewChat">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            <line x1="12" y1="8" x2="12" y2="14"></line>
            <line x1="9" y1="11" x2="15" y2="11"></line>
          </svg>
        </button>
      </header>
      <Chat :token="accessToken"/>
    </div>
  </div>
</template>
