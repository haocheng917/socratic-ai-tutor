<!--
  登录 / 注册页（纯 UI，无业务逻辑）
  - 表单请自行绑定 v-model 与 @submit.prevent="..."
  - 登录 / 注册切换由纯 CSS 的 radio + label 完成，不依赖 JS
-->

<script setup>

import { compile, ref } from 'vue'

const emit = defineEmits(['login-success'])
const baseUrl = import.meta.env.VITE_API_BASE_URL

const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')

async function handleLogin() {
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
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || '登录失败')
    }
    emit('login-success', data.access_token)
  } catch (error) {
    errorMessage.value = error.message || '登录失败'
  }
}

async function handleRegister() {
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
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || '注册失败')
    }
    emit('login-success', data.access_token)
  } catch (error) {
    errorMessage.value = error.message || '注册失败'
  }
}
</script>

<template>
  <div class="auth-page">
    <main class="auth-card">
      <section class="auth-brand" aria-label="AI Tutor 介绍">
        <a class="auth-logo" href="/">
          <span class="auth-logo-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
              stroke-linejoin="round">
              <path
                d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.8 9.8 0 0 1-3.2-.6L4 21l1.7-4.5A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" />
              <path d="M9 10.5h6M9 13.5h3.5" />
            </svg>
          </span>
          <span>AI Tutor</span>
        </a>

        <div class="auth-brand-copy">
          <p class="auth-eyebrow">Socratic Learning</p>
          <h1 class="auth-tagline">好问题，<br /><em>比答案更重要。</em></h1>
          <p class="auth-desc">AI 导师用追问带你拆解难题，让理解真正发生。</p>
        </div>

        <ul class="auth-points">
          <li>
            <svg viewBox="0 0 16 16" aria-hidden="true">
              <path d="m3.4 8.3 3 3 6.2-6.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
            <span>循序渐进，而不是直接给答案</span>
          </li>
          <li>
            <svg viewBox="0 0 16 16" aria-hidden="true">
              <path d="m3.4 8.3 3 3 6.2-6.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
            <span>支持图片提问与多轮对话</span>
          </li>
          <li>
            <svg viewBox="0 0 16 16" aria-hidden="true">
              <path d="m3.4 8.3 3 3 6.2-6.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
            <span>学习记录随时可查</span>
          </li>
        </ul>

        <p class="auth-brand-foot">© 2026 AI Tutor</p>
      </section>

      <section class="auth-panel" aria-label="账号登录与注册">
        <input class="auth-tab-input" type="radio" name="auth-mode" id="auth-mode-login" checked />
        <input class="auth-tab-input" type="radio" name="auth-mode" id="auth-mode-register" />

        <div class="auth-tabs">
          <label for="auth-mode-login">登录</label>
          <label for="auth-mode-register">注册</label>
        </div>

        <!-- 登录表单：绑定 @submit.prevent="handleLogin" -->
        <form class="auth-form auth-form--login" @submit.prevent="handleLogin">
          <header class="auth-head">
            <h2 class="auth-title">欢迎回来</h2>
            <p class="auth-subtitle">登录后继续你的学习旅程。</p>
          </header>

          <p v-if="errorMessage" class="auth-error" role="alert">
            {{ errorMessage }}
          </p>

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

          <button class="auth-submit" type="submit">登录</button>

          <p class="auth-switch">
            还没有账号？<label class="auth-link" for="auth-mode-register">立即注册</label>
          </p>
        </form>

        <!-- 注册表单：绑定 @submit.prevent="handleRegister" -->
        <form class="auth-form auth-form--register" @submit.prevent="handleRegister">
          <header class="auth-head">
            <h2 class="auth-title">创建账号</h2>
            <p class="auth-subtitle">几秒钟开始你的 AI 学习之旅。</p>
          </header>

          <p v-if="errorMessage" class="auth-error" role="alert">
            {{ errorMessage }}
          </p>

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

          <button class="auth-submit" type="submit">创建账号</button>

          <p class="auth-switch">
            已有账号？<label class="auth-link" for="auth-mode-login">去登录</label>
          </p>
        </form>
      </section>
    </main>
  </div>
</template>

<style scoped>
.auth-page {
  --auth-ink: #14211f;
  --auth-muted: #6b7b78;
  --auth-line: #e0e8e5;
  --auth-accent: #0f9b9b;
  --auth-accent-strong: #0b7376;
  --auth-blue: #3b8fd6;

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
  background:
    radial-gradient(900px 520px at 8% 0%, rgba(24, 168, 168, 0.12), transparent 62%),
    radial-gradient(820px 520px at 100% 100%, rgba(59, 143, 214, 0.1), transparent 58%),
    #f3f7f6;
}

.auth-card {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.02fr) minmax(0, 0.98fr);
  width: min(100%, 980px);
  margin: auto;
  overflow: hidden;
  border: 1px solid rgba(15, 60, 60, 0.07);
  border-radius: 28px;
  background: #fff;
  box-shadow:
    0 30px 80px -40px rgba(10, 55, 60, 0.35),
    0 8px 24px -18px rgba(10, 55, 60, 0.2);
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
  background:
    radial-gradient(120% 90% at 100% 0%, rgba(89, 214, 206, 0.28), transparent 55%),
    linear-gradient(155deg, #0b3b40 0%, #0d5c62 55%, #127b85 100%);
}

.auth-brand::before,
.auth-brand::after {
  content: "";
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
  backdrop-filter: blur(6px);
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

.auth-eyebrow {
  margin: 0 0 14px;
  color: rgba(255, 255, 255, 0.55);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.auth-tagline {
  margin: 0;
  font-size: clamp(28px, 3vw, 38px);
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.02em;
}

.auth-tagline em {
  color: #8fe7df;
  font-style: normal;
}

.auth-desc {
  max-width: 30ch;
  margin: 16px 0 0;
  color: rgba(255, 255, 255, 0.68);
  font-size: 13.5px;
  line-height: 1.75;
}

.auth-points {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 11px;
  margin: 32px 0 0;
  padding: 0;
  list-style: none;
}

.auth-points li {
  display: flex;
  align-items: center;
  gap: 10px;
  color: rgba(255, 255, 255, 0.76);
  font-size: 12.5px;
  line-height: 1.5;
}

.auth-points svg {
  flex: none;
  width: 15px;
  height: 15px;
  padding: 2px;
  border-radius: 50%;
  background: rgba(143, 231, 223, 0.14);
  color: #8fe7df;
}

.auth-brand-foot {
  position: relative;
  z-index: 1;
  margin: auto 0 0;
  padding-top: 40px;
  color: rgba(255, 255, 255, 0.38);
  font-size: 10.5px;
  letter-spacing: 0.04em;
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
  border-radius: 12px;
  background: #f0f4f3;
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
  outline: 2px solid rgba(15, 155, 155, 0.55);
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
  background: #fafcfb;
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
  box-shadow: 0 0 0 3px rgba(24, 168, 168, 0.13);
}

.auth-input:-webkit-autofill {
  -webkit-text-fill-color: var(--auth-ink);
  -webkit-box-shadow: 0 0 0 1000px #fafcfb inset;
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
  background: linear-gradient(135deg, #18a8a8, var(--auth-blue));
  box-shadow: 0 12px 24px -14px rgba(15, 155, 155, 0.75);
  font: inherit;
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
}

.auth-submit:hover {
  filter: brightness(1.04);
  box-shadow: 0 14px 28px -14px rgba(15, 155, 155, 0.85);
  transform: translateY(-1px);
}

.auth-submit:active {
  filter: brightness(0.98);
  transform: translateY(0);
}

.auth-submit:focus-visible {
  outline: 3px solid rgba(15, 155, 155, 0.28);
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
  color: #0a6668;
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
    border-radius: 24px;
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

  .auth-eyebrow {
    margin-bottom: 10px;
  }

  .auth-tagline {
    font-size: 27px;
  }

  .auth-desc {
    max-width: 42ch;
    margin-top: 10px;
    font-size: 13px;
  }

  .auth-points,
  .auth-brand-foot {
    display: none;
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
    border-radius: 20px;
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

  .auth-points {
    margin-top: 24px;
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
