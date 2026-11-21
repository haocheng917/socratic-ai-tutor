<!--
  登录 / 注册页（纯 UI，无业务逻辑）
  - 表单请自行绑定 v-model 与 @submit.prevent="..."
  - 登录 / 注册切换由纯 CSS 的 radio + label 完成，不依赖 JS
-->

<script setup>

import { ref } from 'vue'
import ErrorNotice from './ErrorNotice.vue'
import { readError, toErrorMessage } from '../utils/http'

const emit = defineEmits(['login-success'])
const baseUrl = import.meta.env.VITE_API_BASE_URL

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false)

async function handleLogin() {
  if (isSubmitting.value) return
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    const res = await fetch(`${baseUrl}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'username': username.value,
        'password': password.value
      })
    })
    if (!res.ok) {
      throw new Error(await readError(res, '登录失败'))
    }
    const data = await res.json()
    if (!data || !data.access_token) {
      throw new Error('登录失败：服务端未返回令牌')
    }
    emit('login-success', data.access_token)
  } catch (error) {
    errorMessage.value = toErrorMessage(error, '登录失败')
  } finally {
    isSubmitting.value = false
  }
}

async function handleRegister() {
  if (isSubmitting.value) return
  errorMessage.value = ''
  isSubmitting.value = true
  try {
    if (password.value !== confirmPassword.value) {
      throw new Error('两次密码不一致')
    }
    const res = await fetch(`${baseUrl}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        'username': username.value,
        'password': password.value
      })
    })
    if (!res.ok) {
      throw new Error(await readError(res, '注册失败'))
    }
    const data = await res.json()
    if (!data || !data.access_token) {
      throw new Error('注册失败：服务端未返回令牌')
    }
    emit('login-success', data.access_token)
  } catch (error) {
    errorMessage.value = toErrorMessage(error, '注册失败')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <main class="auth-card">
      <section class="auth-brand" aria-label="启问介绍">
        <a class="auth-logo" href="/">
          <span class="auth-logo-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round">
              <path
                d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.8 9.8 0 0 1-3.2-.6L4 21l1.7-4.5A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" />
              <path d="M9 10.5h6M9 13.5h3.5" />
            </svg>
          </span>
          <span>启问</span>
        </a>

        <div class="auth-brand-copy">
          <h1 class="auth-tagline">好问题，<br /><em>比答案更重要。</em></h1>
          <p class="auth-desc">不直接给答案，用一个个问题带你拆解难题，让理解真正发生。</p>
        </div>
      </section>

      <section class="auth-panel" aria-label="账号登录与注册">
        <input class="auth-tab-input" type="radio" name="auth-mode" id="auth-mode-login" checked />
        <input class="auth-tab-input" type="radio" name="auth-mode" id="auth-mode-register" />

        <div class="auth-tabs">
          <label for="auth-mode-login" @click="errorMessage = ''">登录</label>
          <label for="auth-mode-register" @click="errorMessage = ''">注册</label>
        </div>

        <!-- 登录表单：绑定 @submit.prevent="handleLogin" -->
        <form class="auth-form auth-form--login" @submit.prevent="handleLogin">
          <header class="auth-head">
            <h2 class="auth-title">欢迎回来</h2>
            <p class="auth-subtitle">登录后继续你的学习旅程。</p>
          </header>

          <ErrorNotice v-if="errorMessage" title="" :message="errorMessage" @dismiss="errorMessage = ''" />

          <div class="auth-field">
            <label for="login-username">用户名</label>
            <input v-model="username" class="auth-input" id="login-username" name="username" type="text"
              placeholder="请输入用户名" autocomplete="username" required />
          </div>

          <div class="auth-field">
            <label for="login-password">密码</label>
            <input v-model="password" class="auth-input" id="login-password" name="password" type="password"
              placeholder="请输入密码" autocomplete="current-password" required />
          </div>

          <button class="auth-submit" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '登录中…' : '登录' }}
          </button>

          <p class="auth-switch">
            还没有账号？<label class="auth-link" for="auth-mode-register" @click="errorMessage = ''">立即注册</label>
          </p>
        </form>

        <!-- 注册表单：绑定 @submit.prevent="handleRegister" -->
        <form class="auth-form auth-form--register" @submit.prevent="handleRegister">
          <header class="auth-head">
            <h2 class="auth-title">创建账号</h2>
            <p class="auth-subtitle">几秒钟开始你的 AI 学习之旅。</p>
          </header>

          <ErrorNotice v-if="errorMessage" title="" :message="errorMessage" @dismiss="errorMessage = ''" />

          <div class="auth-field">
            <label for="register-username">用户名</label>
            <input v-model="username" class="auth-input" id="register-username" name="username" type="text"
              placeholder="3–20 位字符" autocomplete="username" required minlength="3" maxlength="20" />
          </div>

          <div class="auth-field">
            <label for="register-password">密码</label>
            <input v-model="password" class="auth-input" id="register-password" name="password" type="password"
              placeholder="请设置密码" autocomplete="new-password" required minlength="8" maxlength="32"
              aria-describedby="register-password-hint" />
            <p class="auth-hint" id="register-password-hint">8–32 位字符</p>
          </div>

          <div class="auth-field">
            <label for="register-confirm">确认密码</label>
            <input v-model="confirmPassword" class="auth-input" id="register-confirm" name="confirmPassword"
              type="password" placeholder="请再次输入密码" autocomplete="new-password" required minlength="8" maxlength="32" />
          </div>

          <button class="auth-submit" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '创建中…' : '创建账号' }}
          </button>

          <p class="auth-switch">
            已有账号？<label class="auth-link" for="auth-mode-login" @click="errorMessage = ''">去登录</label>
          </p>
        </form>
      </section>
    </main>
  </div>
</template>

<style scoped>
.auth-page {
  --auth-ink: #1f2421;
  --auth-muted: #6a706b;
  --auth-line: #e5e7e3;
  --auth-accent: #2f6b57;
  --auth-accent-strong: #245444;

  height: 100dvh;
  min-height: 100dvh;
  width: 100%;
  padding: 32px;
  overflow-y: auto;
  display: flex;
  color: var(--auth-ink);
  color-scheme: light;
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", system-ui, -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  background: #ffffff;
}

.auth-card {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.02fr) minmax(0, 0.98fr);
  width: min(100%, 980px);
  margin: auto;
  overflow: hidden;
  border: 1px solid var(--auth-line);
  border-radius: 20px;
  background: #fff;
  box-shadow: 0 20px 50px -40px rgba(31, 36, 33, 0.4);
  animation: auth-rise 0.5s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

/* ---------- 左侧品牌区 ---------- */

.auth-brand {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 42px 44px 32px;
  overflow: hidden;
  color: #fff;
  background: #233029;
}

.auth-brand::before,
.auth-brand::after {
  content: "";
  display: none;
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.12);
  pointer-events: none;
}

.auth-brand::before {
  width: 420px;
  height: 420px;
  top: -170px;
  right: -210px;
}

.auth-brand::after {
  width: 280px;
  height: 280px;
  right: -80px;
  bottom: -150px;
  border-color: rgba(255, 255, 255, 0.08);
}

.auth-logo {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  align-self: flex-start;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-decoration: none;
}

.auth-logo-mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 11px;
  background: rgba(255, 255, 255, 0.11);
}

.auth-logo-mark svg {
  width: 21px;
  height: 21px;
}

.auth-brand-copy {
  position: relative;
  z-index: 1;
  margin-top: clamp(48px, 8vh, 84px);
}


.auth-tagline {
  margin: 0;
  font-size: clamp(28px, 3vw, 38px);
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.02em;
}

.auth-tagline em {
  color: #cfe0d5;
  font-style: normal;
}

.auth-desc {
  max-width: 30ch;
  margin: 16px 0 0;
  color: rgba(255, 255, 255, 0.68);
  font-size: 13.5px;
  line-height: 1.75;
}


/* ---------- 右侧表单区 ---------- */

.auth-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 48px 44px;
  background: #fff;
}

/* 真实 radio 只做状态机，视觉上隐藏但保留键盘焦点 */
.auth-tab-input {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0 0 0 0);
  white-space: nowrap;
  border: 0;
}

.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  margin-bottom: 30px;
  padding: 4px;
  border-radius: 10px;
  background: #f3f4f2;
}

.auth-tabs label {
  padding: 10px 12px;
  border-radius: 9px;
  color: var(--auth-muted);
  font-size: 13.5px;
  font-weight: 600;
  text-align: center;
  cursor: pointer;
  user-select: none;
  transition: color 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
}

.auth-tabs label:hover {
  color: var(--auth-accent-strong);
}

#auth-mode-login:checked~.auth-tabs label[for="auth-mode-login"],
#auth-mode-register:checked~.auth-tabs label[for="auth-mode-register"] {
  color: var(--auth-accent-strong);
  background: #fff;
  box-shadow:
    0 1px 2px rgba(16, 50, 50, 0.08),
    0 2px 6px -2px rgba(16, 50, 50, 0.12);
}

#auth-mode-login:focus-visible~.auth-tabs label[for="auth-mode-login"],
#auth-mode-register:focus-visible~.auth-tabs label[for="auth-mode-register"] {
  outline: 2px solid rgba(47, 107, 87, 0.55);
  outline-offset: 2px;
}

.auth-form {
  display: none;
  flex-direction: column;
  animation: auth-fade 0.22s ease both;
}

#auth-mode-login:checked~.auth-form--login,
#auth-mode-register:checked~.auth-form--register {
  display: flex;
}

.auth-title {
  margin: 0;
  color: #12201f;
  font-size: 26px;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.03em;
}

.auth-subtitle {
  margin: 8px 0 26px;
  color: var(--auth-muted);
  font-size: 13px;
  line-height: 1.6;
}

.auth-error {
  margin: 0 0 16px;
  padding: 10px 12px;
  border: 1px solid #f3d3cf;
  border-radius: 10px;
  background: #fff6f5;
  color: #b44136;
  font-size: 12.5px;
  line-height: 1.5;
}

.auth-form .error-notice {
  margin-bottom: 16px;
}

.auth-error:empty {
  display: none;
}

.auth-field {
  display: flex;
  flex-direction: column;
  gap: 7px;
  margin-bottom: 16px;
}

.auth-field>label {
  color: #33433f;
  font-size: 12.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.auth-input {
  width: 100%;
  height: 48px;
  padding: 0 14px;
  border: 1px solid var(--auth-line);
  border-radius: 12px;
  outline: none;
  background: #fff;
  color: var(--auth-ink);
  font: inherit;
  font-size: 14px;
  transition: border-color 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
}

.auth-input::placeholder {
  color: #a9b5b2;
}

.auth-input:hover {
  border-color: #cfdad7;
}

.auth-input:focus {
  border-color: var(--auth-accent);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(47, 107, 87, 0.14);
}

.auth-input:-webkit-autofill {
  -webkit-text-fill-color: var(--auth-ink);
  -webkit-box-shadow: 0 0 0 1000px #ffffff inset;
}

.auth-hint {
  margin: -1px 0 0;
  color: #8a9996;
  font-size: 11.5px;
  line-height: 1.5;
}

.auth-submit {
  width: 100%;
  height: 48px;
  margin-top: 2px;
  border: 0;
  border-radius: 12px;
  color: #fff;
  background: var(--auth-accent);
  box-shadow: 0 10px 22px -18px rgba(35, 83, 67, 0.8);
  font: inherit;
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
}

.auth-submit:hover {
  background: var(--auth-accent-strong);
  box-shadow: 0 12px 24px -18px rgba(35, 83, 67, 0.9);
  transform: translateY(-1px);
}

.auth-submit:active {
  background: var(--auth-accent-strong);
  transform: translateY(0);
}

.auth-submit:focus-visible {
  outline: 3px solid rgba(47, 107, 87, 0.3);
  outline-offset: 2px;
}

.auth-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.auth-switch {
  margin: 20px 0 0;
  color: #7c8b88;
  font-size: 12.5px;
  text-align: center;
}

.auth-link {
  color: var(--auth-accent-strong);
  font-weight: 600;
  cursor: pointer;
}

.auth-link:hover {
  color: #1c4236;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.auth-form--register .auth-submit {
  margin-top: 6px;
}

/* ---------- 响应式 ---------- */

@media (max-width: 900px) {
  .auth-page {
    padding: 20px;
  }

  .auth-card {
    grid-template-columns: 1fr;
    width: min(100%, 540px);
    border-radius: 18px;
  }

  .auth-brand {
    padding: 26px 28px 24px;
  }

  .auth-brand::before {
    width: 300px;
    height: 300px;
    top: -150px;
    right: -150px;
  }

  .auth-brand-copy {
    margin-top: 30px;
  }


  .auth-tagline {
    font-size: 27px;
  }

  .auth-desc {
    max-width: 42ch;
    margin-top: 10px;
    font-size: 13px;
  }

  .auth-panel {
    padding: 30px 28px 34px;
  }

  .auth-tabs {
    margin-bottom: 26px;
  }
}

@media (max-width: 480px) {
  .auth-page {
    padding: 12px;
  }

  .auth-card {
    border-radius: 16px;
  }

  .auth-brand {
    padding: 22px 20px 20px;
  }

  .auth-tagline {
    font-size: 23px;
  }

  .auth-desc {
    display: none;
  }

  .auth-panel {
    padding: 24px 20px 28px;
  }

  .auth-title {
    font-size: 22px;
  }

  .auth-subtitle {
    margin-bottom: 22px;
  }
}

@media (max-height: 760px) and (min-width: 901px) {
  .auth-brand {
    padding: 32px 40px 26px;
  }

  .auth-brand-copy {
    margin-top: 36px;
  }

  .auth-tagline {
    font-size: 30px;
  }

  .auth-panel {
    padding: 34px 40px;
  }
}

/* ---------- 动效 ---------- */

@keyframes auth-rise {
  from {
    opacity: 0;
    transform: translateY(14px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

@keyframes auth-fade {
  from {
    opacity: 0;
    transform: translateY(4px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {

  .auth-card,
  .auth-form {
    animation: none !important;
  }

  .auth-tabs label,
  .auth-input,
  .auth-submit {
    transition: none !important;
  }
}
</style>
