<script setup>
defineProps({
  message: { type: String, default: '' },
  title: { type: String, default: '出错了' },
  dismissible: { type: Boolean, default: true },
})

defineEmits(['dismiss'])
</script>

<template>
  <div v-if="message" class="error-notice" role="alert" aria-live="assertive">
    <span class="error-notice-icon" aria-hidden="true">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
        stroke-linejoin="round">
        <circle cx="12" cy="12" r="9" />
        <line x1="12" y1="7.5" x2="12" y2="13" />
        <line x1="12" y1="16.5" x2="12.01" y2="16.5" />
      </svg>
    </span>

    <div class="error-notice-body">
      <p v-if="title" class="error-notice-title">{{ title }}</p>
      <p class="error-notice-text">{{ message }}</p>
    </div>

    <button v-if="dismissible" class="error-notice-close" type="button" aria-label="关闭错误提示" @click="$emit('dismiss')">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="6" y1="6" x2="18" y2="18" />
        <line x1="18" y1="6" x2="6" y2="18" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.error-notice {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 11px 12px;
  border: 1px solid #f2cfca;
  border-radius: 12px;
  background: linear-gradient(180deg, #fff8f7, #fff3f1);
  color: #8f3029;
  box-shadow: 0 6px 18px -14px rgba(180, 65, 54, 0.7);
  animation: error-in 0.22s ease both;
}

.error-notice-icon {
  display: grid;
  place-items: center;
  flex: none;
  width: 22px;
  height: 22px;
  margin-top: 1px;
  border-radius: 50%;
  background: rgba(196, 65, 54, 0.1);
  color: #c2413a;
}

.error-notice-icon svg {
  width: 15px;
  height: 15px;
}

.error-notice-body {
  flex: 1;
  min-width: 0;
}

.error-notice-title {
  margin: 0 0 2px;
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.error-notice-text {
  margin: 0;
  font-size: 13px;
  line-height: 1.55;
  word-break: break-word;
}

.error-notice-close {
  display: grid;
  place-items: center;
  flex: none;
  width: 24px;
  height: 24px;
  padding: 0;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: #b46860;
  cursor: pointer;
  transition: background 0.16s ease, color 0.16s ease;
}

.error-notice-close:hover {
  background: rgba(196, 65, 54, 0.1);
  color: #8f3029;
}

.error-notice-close:focus-visible {
  outline: 2px solid rgba(196, 65, 54, 0.4);
  outline-offset: 1px;
}

.error-notice-close svg {
  width: 14px;
  height: 14px;
}

@keyframes error-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .error-notice {
    animation: none;
  }
}
</style>
