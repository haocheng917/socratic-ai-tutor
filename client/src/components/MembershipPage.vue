<!--
  会员中心页
  - 套餐：全部来自 GET /membership/plans（含 free）
  - 仅 UI 与套餐加载，不含下单/支付逻辑
  - 点击「返回」会向父组件派发 close 事件：<MembershipPage @close="..." />
-->

<script setup>
import { onMounted, ref } from 'vue'
import ErrorNotice from './ErrorNotice.vue'
import { readError, toErrorMessage } from '../utils/http.js'

defineEmits(['close'])

const baseUrl = import.meta.env.VITE_API_BASE_URL

const plans = ref([])
const isLoading = ref(true)
const loadError = ref('')

/* 套餐展示文案：code 与后端 MEMBERSHIP_PLANS 对应 */
const PLAN_META = {
  free: {
    name: '轻享版',
    desc: '偶尔来问，够用就好',
    tone: 'sage',
    cta: '免费开始',
    recommended: false,
  },
  plus: {
    name: '进阶版',
    desc: '高频学习者的日常选择',
    tone: 'green',
    cta: '选择进阶版',
    recommended: false,
  },
  pro: {
    name: '尊享版',
    desc: '为长期目标配一位学习搭档',
    tag: '长期备考',
    tone: 'gold',
    cta: '选择尊享版',
    recommended: false,
  },
}

function formatPrice(value) {
  const cents = Number(value)
  if (!Number.isFinite(cents)) return '--'
  const yuan = cents / 100
  if (Number.isInteger(yuan)) return String(yuan)
  return yuan.toFixed(2).replace(/0+$/, '').replace(/\.$/, '')
}

function formatPeriod(days) {
  const n = Number(days)
  if (!Number.isFinite(n) || n <= 0) return '/ 永久'
  if (n === 30) return '/ 月'
  if (n === 365) return '/ 年'
  return `/ ${n} 天`
}

function normalizePlan(plan, index) {
  const code = plan?.code || `plan-${index}`
  const meta = PLAN_META[code] || {}
  const durationDays = Number(plan?.duration_days)
  const recommended = meta.recommended === true
  const name = meta.name || plan?.name || code

  return {
    code,
    name,
    desc: meta.desc || (durationDays > 0 ? `有效期 ${durationDays} 天` : ''),
    badge: meta.badge || (recommended ? '最受欢迎' : ''),
    tag: meta.tag || '',
    tone: meta.tone || 'sage',
    price: Number(plan?.price) || 0,
    period: formatPeriod(durationDays),
    features: Array.isArray(plan?.describe) ? plan.describe.filter(Boolean) : [],
    cta: meta.cta || `选择${name}`,
    recommended,
  }
}

function normalizePlans(data) {
  const list = Array.isArray(data) ? data : Array.isArray(data?.plans) ? data.plans : []
  return list
    .filter((plan) => plan && plan.code)
    .sort((a, b) => Number(a.price) - Number(b.price))
    .map(normalizePlan)
}

async function getPlans() {
  isLoading.value = true
  loadError.value = ''

  try {
    const res = await fetch(`${baseUrl}/membership/plans`, {
      headers: { Accept: 'application/json' },
    })
    if (!res.ok) {
      throw new Error(await readError(res, '加载会员方案失败'))
    }
    plans.value = normalizePlans(await res.json())
  } catch (error) {
    console.error(error)
    plans.value = []
    loadError.value = toErrorMessage(error, '加载会员方案失败')
  } finally {
    isLoading.value = false
  }
}

onMounted(getPlans)
</script>

<template>
  <div class="membership-page">
    <header class="membership-nav">
      <a class="membership-brand" href="/" aria-label="启问首页">
        <span class="membership-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"
            stroke-linejoin="round">
            <path
              d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.8 9.8 0 0 1-3.2-.6L4 21l1.7-4.5A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" />
            <path d="M9 10.5h6M9 13.5h3.5" />
          </svg>
        </span>
        <span>启问</span>
      </a>

      <span class="membership-nav-divider" aria-hidden="true"></span>
      <span class="membership-nav-label">会员中心</span>

      <button class="membership-back" type="button" aria-label="返回对话" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"
          stroke-linejoin="round" aria-hidden="true">
          <path d="m15 18-6-6 6-6" />
        </svg>
        <span>返回</span>
      </button>
    </header>

    <main class="membership-main">
      <section class="membership-hero" aria-labelledby="membership-title">
        <h1 id="membership-title" class="membership-title">升级成启问会员</h1>
      </section>

      <section class="membership-plans" aria-label="会员方案" :aria-busy="isLoading">
        <template v-if="isLoading">
          <div v-for="n in 3" :key="`skeleton-${n}`" class="membership-plan membership-plan--skeleton"
            aria-hidden="true">
            <span class="skeleton-line skeleton-line--title"></span>
            <span class="skeleton-line skeleton-line--desc"></span>
            <span class="skeleton-line skeleton-line--price"></span>
            <span class="skeleton-line"></span>
            <span class="skeleton-line"></span>
            <span class="skeleton-line skeleton-line--short"></span>
            <span class="skeleton-line skeleton-line--button"></span>
          </div>
        </template>

        <div v-else-if="loadError" class="membership-plans-state">
          <ErrorNotice title="没能加载会员方案" :message="loadError" :dismissible="false" />
          <button class="membership-state-retry" type="button" @click="getPlans">再试一次</button>
        </div>

        <template v-else>
          <article v-for="plan in plans" :key="plan.code" class="membership-plan"
            :class="[`membership-plan--${plan.tone}`, { 'membership-plan--pro': plan.recommended }]">
            <header class="plan-head">
              <div class="plan-title-row">
                <h2 class="plan-name">{{ plan.name }}</h2>
                <span v-if="plan.badge" class="plan-badge">{{ plan.badge }}</span>
                <span v-else-if="plan.tag" class="plan-tag">{{ plan.tag }}</span>
              </div>
              <p v-if="plan.desc" class="plan-desc">{{ plan.desc }}</p>
            </header>

            <p class="plan-price">
              <span class="plan-currency">¥</span>
              <span class="plan-amount">{{ formatPrice(plan.price) }}</span>
              <span class="plan-period">{{ plan.period }}</span>
            </p>

            <ul class="plan-features">
              <li v-for="feature in plan.features" :key="feature">{{ feature }}</li>
            </ul>

            <button class="plan-btn" :class="{ 'plan-btn--primary': plan.recommended }" type="button">
              {{ plan.cta }}
            </button>
          </article>
        </template>
      </section>

      <p class="membership-footnote">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"
          stroke-linejoin="round" aria-hidden="true">
          <path d="M12 3 5 6v5c0 4.4 3 8.4 7 10 4-1.6 7-5.6 7-10V6l-7-3Z" />
          <path d="m9.5 12 1.8 1.8 3.4-3.6" />
        </svg>
        所有方案均支持随时取消；已购时长到期前权益持续有效。
      </p>
    </main>
  </div>
</template>

<style scoped>
.membership-page {
  --membership-ink: #1f2421;
  --membership-ink-soft: #3a403c;
  --membership-muted: #6a706b;
  --membership-muted-soft: #8d938e;
  --membership-line: #e5e7e3;
  --membership-line-strong: #d4d7d1;
  --membership-accent: #2f6b57;
  --membership-accent-strong: #245444;
  --membership-accent-soft: #edf3f0;
  --membership-paper: #ffffff;

  height: 100dvh;
  min-height: 100dvh;
  width: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  color: var(--membership-ink);
  color-scheme: light;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", "Noto Sans SC", system-ui,
    -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  background:
    radial-gradient(920px 420px at 50% -180px, #e8f1eb 0%, rgba(232, 241, 235, 0) 72%),
    var(--membership-paper);
  scrollbar-width: thin;
  scrollbar-color: #d8d3c7 transparent;
}

.membership-page::-webkit-scrollbar {
  width: 8px;
}

.membership-page::-webkit-scrollbar-thumb {
  border: 2px solid transparent;
  border-radius: 999px;
  background: #d8d3c7;
  background-clip: content-box;
}

.membership-page *,
.membership-page *::before,
.membership-page *::after {
  box-sizing: border-box;
}

/* ---------- 进入动画 ---------- */

.membership-page {
  animation: membership-page-fade 0.24s ease-out both;
}

.membership-nav {
  animation: membership-nav-fade 0.3s ease-out both;
}

.membership-hero {
  animation: membership-rise 0.42s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

.membership-plan {
  animation: membership-plan-pop 0.46s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

.membership-plan:nth-child(1) {
  animation-delay: 0.06s;
}

.membership-plan:nth-child(2) {
  animation-delay: 0.13s;
}

.membership-plan:nth-child(3) {
  animation-delay: 0.2s;
}

.membership-footnote {
  animation: membership-rise 0.4s ease-out 0.3s both;
}

@keyframes membership-page-fade {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes membership-nav-fade {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes membership-rise {
  from {
    opacity: 0;
    translate: 0 10px;
  }

  to {
    opacity: 1;
    translate: 0 0;
  }
}

@keyframes membership-plan-pop {
  from {
    opacity: 0;
    translate: 0 14px;
    scale: 0.96;
  }

  to {
    opacity: 1;
    translate: 0 0;
    scale: 1;
  }
}

@keyframes membership-plan-skeleton {
  from {
    background-position: 100% 50%;
  }

  to {
    background-position: 0 50%;
  }
}


/* ---------- 顶部导航 ---------- */

.membership-nav {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 12px;
  height: 56px;
  padding: 0 clamp(16px, 4vw, 40px);
  border-bottom: 1px solid rgba(229, 231, 227, 0.85);
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.membership-brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--membership-ink);
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
  text-decoration: none;
}

.membership-brand-mark {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border: 1px solid #d3e4da;
  border-radius: 8px;
  background: var(--membership-accent-soft);
  color: var(--membership-accent-strong);
}

.membership-brand-mark svg {
  width: 18px;
  height: 18px;
}

.membership-nav-divider {
  width: 1px;
  height: 16px;
  background: var(--membership-line-strong);
}

.membership-nav-label {
  margin-right: auto;
  color: var(--membership-muted);
  font-size: 12.5px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.membership-back {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 34px;
  padding: 0 12px 0 9px;
  border: 1px solid var(--membership-line);
  border-radius: 9px;
  background: #fff;
  color: var(--membership-ink-soft);
  font: inherit;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}

.membership-back svg {
  width: 16px;
  height: 16px;
}

.membership-back:hover {
  border-color: var(--membership-accent);
  background: var(--membership-accent-soft);
  color: var(--membership-accent-strong);
}

/* ---------- 页面主体 ---------- */

.membership-main {
  width: min(100%, 1080px);
  margin: 0 auto;
  padding: clamp(20px, 3.6vw, 32px) clamp(20px, 4vw, 32px) 24px;
}

.membership-hero {
  max-width: 680px;
  margin: 0 auto clamp(20px, 2.8vw, 30px);
  text-align: center;
}

.membership-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border: 1px solid #d9e5de;
  border-radius: 999px;
  background: rgba(237, 243, 240, 0.8);
  color: var(--membership-accent-strong);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.membership-eyebrow svg {
  width: 12px;
  height: 12px;
}

.membership-title {
  margin: 12px 0 8px;
  color: var(--membership-ink);
  font-size: clamp(27px, 3.4vw, 40px);
  font-weight: 650;
  letter-spacing: -0.03em;
  line-height: 1.22;
  text-wrap: balance;
}

.membership-title em {
  color: var(--membership-accent);
  font-style: normal;
}

.membership-subtitle {
  max-width: 540px;
  margin: 0 auto;
  color: var(--membership-muted);
  font-size: clamp(13px, 1.3vw, 14.5px);
  line-height: 1.65;
  text-wrap: balance;
}

/* ---------- 三档方案 ---------- */

.membership-plans {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(12px, 1.6vw, 18px);
  align-items: stretch;
}

.membership-plan {
  --plan-accent: #6f8779;
  --plan-soft: #f2f6f3;
  --plan-tint: #fbfcfa;
  --plan-line: #e2eae4;

  position: relative;
  display: flex;
  flex-direction: column;
  padding: clamp(20px, 2vw, 24px);
  border: 1px solid var(--plan-line);
  border-radius: 16px;
  background: linear-gradient(180deg, var(--plan-tint) 0%, #fff 44%);
  box-shadow: 0 1px 2px rgba(35, 40, 36, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.membership-plan:hover {
  transform: translateY(-2px);
  border-color: var(--membership-line-strong);
  box-shadow: 0 22px 42px -34px rgba(31, 36, 33, 0.32);
}

.membership-plan--sage {
  --plan-accent: #6f8779;
  --plan-soft: #f1f6f3;
  --plan-tint: #fafcfa;
  --plan-line: #e2eae4;
}

.membership-plan--green {
  --plan-accent: #40745f;
  --plan-soft: #edf4f0;
  --plan-tint: #f8fbf9;
  --plan-line: #dce9e2;
}

.membership-plan--gold {
  --plan-accent: #9d7a2a;
  --plan-soft: #faf3e2;
  --plan-tint: #fdfaf2;
  --plan-line: #eee1c4;
}

.membership-plan--pro {
  border-color: #bcd6c8;
  background:
    radial-gradient(120% 90% at 100% 0%, rgba(47, 107, 87, 0.1) 0%, rgba(47, 107, 87, 0) 58%),
    #f5f9f7;
  box-shadow: 0 18px 38px -32px rgba(47, 107, 87, 0.5);
}

.membership-plan--pro:hover {
  border-color: var(--membership-accent);
  box-shadow: 0 24px 46px -32px rgba(47, 107, 87, 0.55);
}

/* ---------- 加载 / 错误状态 ---------- */

.membership-plan--skeleton {
  gap: 12px;
  min-height: 280px;
  pointer-events: none;
}

.membership-plan--skeleton:hover {
  transform: none;
  border-color: var(--membership-line);
  box-shadow: 0 1px 2px rgba(35, 40, 36, 0.04);
}

.skeleton-line {
  display: block;
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, #f1f3ef 25%, #e7eae4 37%, #f1f3ef 63%);
  background-size: 400% 100%;
  animation: membership-plan-skeleton 1.4s ease infinite;
}

.skeleton-line--title {
  width: 42%;
  height: 18px;
}

.skeleton-line--desc {
  width: 64%;
}

.skeleton-line--price {
  width: 36%;
  height: 34px;
  margin: 6px 0 4px;
}

.skeleton-line--short {
  width: 74%;
}

.skeleton-line--button {
  width: 100%;
  height: 40px;
  margin-top: auto;
}

.membership-plans-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  border: 1px solid var(--membership-line);
  border-radius: 16px;
  background: #fbfcfa;
}

.membership-plans-state .error-notice {
  width: min(100%, 520px);
}

.membership-state-retry {
  height: 38px;
  padding: 0 18px;
  border: 1px solid var(--membership-line-strong);
  border-radius: 9px;
  background: #fff;
  color: var(--membership-ink-soft);
  font: inherit;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}

.membership-state-retry:hover {
  border-color: var(--membership-accent);
  background: var(--membership-accent-soft);
  color: var(--membership-accent-strong);
}

.plan-head {
  min-height: 44px;
}

.plan-title-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.plan-name {
  margin: 0;
  color: var(--membership-ink);
  font-size: 17.5px;
  font-weight: 600;
  letter-spacing: -0.01em;
  line-height: 1.3;
}

.plan-badge,
.plan-tag {
  display: inline-flex;
  align-items: center;
  height: 21px;
  padding: 0 8px;
  border-radius: 999px;
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
  white-space: nowrap;
}

.plan-badge {
  background: #dcebe2;
  color: #23523f;
}

.plan-tag {
  border: 1px solid var(--plan-line);
  background: var(--plan-soft);
  color: var(--plan-accent);
}

.plan-desc {
  margin: 4px 0 0;
  color: var(--membership-muted);
  font-size: 12px;
  line-height: 1.5;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin: 16px 0 0;
  color: var(--membership-ink);
  line-height: 1;
}

.plan-currency {
  font-size: 17px;
  font-weight: 600;
}

.plan-amount {
  font-size: clamp(34px, 3.4vw, 42px);
  font-weight: 680;
  letter-spacing: -0.04em;
}

.plan-period {
  margin-left: 4px;
  color: var(--membership-muted-soft);
  font-size: 12px;
  font-weight: 500;
}

.plan-note {
  margin: 7px 0 0;
  color: var(--membership-muted-soft);
  font-size: 11.5px;
  line-height: 1.5;
}

.plan-features {
  flex: 1;
  display: grid;
  align-content: start;
  gap: 8px;
  margin: 16px 0 18px;
  padding: 14px 0 0;
  border-top: 1px solid var(--membership-line);
  list-style: none;
}

.membership-plan--pro .plan-features {
  border-top-color: rgba(47, 107, 87, 0.16);
}

.plan-features li {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: var(--membership-ink-soft);
  font-size: 13px;
  line-height: 1.5;
}

.plan-features li::before {
  content: "✓";
  display: grid;
  place-items: center;
  flex: none;
  width: 16px;
  height: 16px;
  margin-top: 1px;
  border-radius: 50%;
  background: var(--plan-soft);
  color: var(--plan-accent);
  font-size: 9.5px;
  font-weight: 700;
  line-height: 1;
}

.membership-plan--pro .plan-features li::before {
  background: #e0eee6;
  color: var(--membership-accent-strong);
}

.plan-btn {
  width: 100%;
  height: 40px;
  margin-top: auto;
  border: 1px solid var(--membership-line-strong);
  border-radius: 10px;
  background: #fff;
  color: var(--membership-ink);
  font: inherit;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}

.plan-btn:hover {
  border-color: var(--plan-accent);
  background: var(--plan-soft);
  color: var(--plan-accent);
}

.membership-plan--pro .plan-btn--primary {
  border-color: #bcd6c8;
  background: #dcebe2;
  color: var(--membership-accent-strong);
}

.membership-plan--pro .plan-btn--primary:hover {
  border-color: var(--membership-accent);
  background: #cfe3d8;
  color: #1d4536;
}

/* ---------- 页脚说明 ---------- */

.membership-footnote {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  margin: 18px 0 0;
  color: var(--membership-muted-soft);
  font-size: 11.5px;
  line-height: 1.6;
  text-align: center;
}

.membership-footnote svg {
  flex: none;
  width: 14px;
  height: 14px;
}

/* ---------- 平板 / 手机 ---------- */

@media (max-width: 900px) {
  .membership-nav {
    height: 52px;
  }

  .membership-main {
    padding-top: 22px;
    padding-bottom: 26px;
  }

  .membership-hero {
    margin-bottom: 18px;
  }

  .membership-plans {
    grid-template-columns: minmax(0, 1fr);
    max-width: 500px;
    margin: 0 auto;
    gap: 12px;
  }

  .membership-plan {
    padding: 20px;
  }

  .membership-plan:hover {
    transform: none;
  }

  .plan-amount {
    font-size: 36px;
  }

  .plan-features {
    margin: 14px 0 16px;
    padding-top: 12px;
  }
}

@media (max-width: 520px) {
  .membership-nav {
    gap: 10px;
    padding: 0 12px;
  }

  .membership-brand {
    margin-right: auto;
    font-size: 13.5px;
  }

  .membership-brand-mark {
    width: 28px;
    height: 28px;
  }

  .membership-brand-mark svg {
    width: 16px;
    height: 16px;
  }

  .membership-nav-divider,
  .membership-nav-label {
    display: none;
  }

  .membership-back {
    gap: 2px;
    padding: 0 9px 0 6px;
  }

  .membership-back span {
    display: none;
  }

  .membership-main {
    padding: 18px 12px 20px;
  }

  .membership-eyebrow {
    display: none;
  }

  .membership-title {
    margin: 0 0 6px;
    font-size: 24px;
    line-height: 1.3;
  }

  .membership-subtitle {
    font-size: 12px;
    line-height: 1.6;
  }

  .membership-hero {
    margin-bottom: 14px;
  }

  .membership-plans {
    gap: 10px;
  }

  .membership-plan {
    padding: 16px;
    border-radius: 14px;
  }

  .plan-head {
    min-height: 0;
  }

  .plan-name {
    font-size: 16px;
  }

  .plan-desc {
    margin-top: 3px;
    font-size: 11.5px;
  }

  .plan-price {
    margin-top: 10px;
  }

  .plan-currency {
    font-size: 15px;
  }

  .plan-amount {
    font-size: 30px;
  }

  .plan-period {
    font-size: 11px;
  }

  .plan-note {
    display: none;
  }

  .plan-features {
    gap: 5px;
    margin: 10px 0 12px;
    padding-top: 10px;
  }

  .plan-features li {
    gap: 7px;
    font-size: 12.5px;
    line-height: 1.5;
  }

  .plan-features li::before {
    width: 14px;
    height: 14px;
    margin-top: 2px;
    font-size: 8.5px;
  }

  .plan-btn {
    height: 38px;
    font-size: 13px;
    border-radius: 9px;
  }

  .membership-footnote {
    align-items: flex-start;
    margin-top: 14px;
    padding: 0 2px;
    font-size: 11px;
    line-height: 1.55;
    text-align: left;
  }
}

@media (prefers-reduced-motion: reduce) {

  .membership-plan,
  .membership-back,
  .plan-btn {
    transition: none;
  }

  .membership-plan:hover {
    transform: none;
  }
}
</style>

<!--
  用法（父组件中）：
  import MembershipPage from './components/MembershipPage.vue'

  <MembershipPage v-if="showMembership" @close="showMembership = false" />

  建议放在 App.vue 根层级，用 v-if 整页切换；membership-page 自带 100dvh 与滚动。
-->
