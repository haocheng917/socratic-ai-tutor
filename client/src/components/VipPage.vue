<!--
  会员中心页（纯 UI：template + css + close 事件声明，无会员/支付逻辑）
  - 点击「返回」会向父组件派发 close 事件：<VipPage @close="..." />
-->

<script setup>
defineEmits(['close'])
</script>

<template>
  <div class="vip-page">
    <header class="vip-nav">
      <a class="vip-brand" href="/" aria-label="启问首页">
        <span class="vip-brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"
            stroke-linejoin="round">
            <path
              d="M21 11.5a8.4 8.4 0 0 1-8.5 8.3 9.8 9.8 0 0 1-3.2-.6L4 21l1.7-4.5A8 8 0 0 1 4 11.5 8.4 8.4 0 0 1 12.5 3 8.4 8.4 0 0 1 21 11.5Z" />
            <path d="M9 10.5h6M9 13.5h3.5" />
          </svg>
        </span>
        <span>启问</span>
      </a>

      <span class="vip-nav-divider" aria-hidden="true"></span>
      <span class="vip-nav-label">会员中心</span>

      <button class="vip-back" type="button" aria-label="返回对话" @click="$emit('close')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"
          stroke-linejoin="round" aria-hidden="true">
          <path d="m15 18-6-6 6-6" />
        </svg>
        <span>返回</span>
      </button>
    </header>

    <main class="vip-main">
      <section class="vip-hero" aria-labelledby="vip-title">
        <h1 id="vip-title" class="vip-title">升级成启问会员</h1>
      </section>

      <section class="vip-plans" aria-label="会员方案">
        <!-- 轻享版 -->
        <article class="vip-plan">
          <header class="plan-head">
            <div class="plan-title-row">
              <h2 class="plan-name">轻享版</h2>
            </div>
            <p class="plan-desc">偶尔来问，够用就好</p>
          </header>

          <p class="plan-price">
            <span class="plan-currency">¥</span>
            <span class="plan-amount">0</span>
            <span class="plan-period">/ 永久</span>
          </p>

          <ul class="plan-features">
            <li>每日 20 次提问</li>
            <li>基础题目拆解与追问</li>
          </ul>

          <button class="plan-btn" type="button">免费开始</button>
        </article>

        <!-- 进阶版（推荐） -->
        <article class="vip-plan vip-plan--pro">
          <header class="plan-head">
            <div class="plan-title-row">
              <h2 class="plan-name">进阶版</h2>
              <span class="plan-badge">最受欢迎</span>
            </div>
            <p class="plan-desc">高频学习者的日常选择</p>
          </header>

          <p class="plan-price">
            <span class="plan-currency">¥</span>
            <span class="plan-amount">29</span>
            <span class="plan-period">/ 月</span>
          </p>

          <ul class="plan-features">
            <li>每日 200 次提问</li>
            <li>优先响应，减少等待</li>
            <li>无限期保存对话记录</li>
          </ul>

          <button class="plan-btn plan-btn--primary" type="button">选择进阶版</button>
        </article>

        <!-- 尊享版 -->
        <article class="vip-plan vip-plan--max">
          <header class="plan-head">
            <div class="plan-title-row">
              <h2 class="plan-name">尊享版</h2>
            </div>
            <p class="plan-desc">为长期目标配一位学习搭档</p>
          </header>

          <p class="plan-price">
            <span class="plan-currency">¥</span>
            <span class="plan-amount">69</span>
            <span class="plan-period">/ 月</span>
          </p>

          <ul class="plan-features">
            <li>无限次提问</li>
            <li>多设备同步与对话导出</li>
            <li>每月一次学习顾问沟通</li>
          </ul>

          <button class="plan-btn" type="button">选择尊享版</button>
        </article>
      </section>

      <p class="vip-footnote">
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
.vip-page {
  --vip-ink: #1f2421;
  --vip-ink-soft: #3a403c;
  --vip-muted: #6a706b;
  --vip-muted-soft: #8d938e;
  --vip-line: #e5e7e3;
  --vip-line-strong: #d4d7d1;
  --vip-accent: #2f6b57;
  --vip-accent-strong: #245444;
  --vip-accent-soft: #edf3f0;
  --vip-paper: #ffffff;

  height: 100dvh;
  min-height: 100dvh;
  width: 100%;
  overflow-x: hidden;
  overflow-y: auto;
  color: var(--vip-ink);
  color-scheme: light;
  font-family: "Inter", "HarmonyOS Sans SC", "PingFang SC", "Microsoft YaHei", "Noto Sans SC", system-ui,
    -apple-system, sans-serif;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  background:
    radial-gradient(920px 420px at 50% -180px, #e8f1eb 0%, rgba(232, 241, 235, 0) 72%),
    var(--vip-paper);
  scrollbar-width: thin;
  scrollbar-color: #d8d3c7 transparent;
}

.vip-page::-webkit-scrollbar {
  width: 8px;
}

.vip-page::-webkit-scrollbar-thumb {
  border: 2px solid transparent;
  border-radius: 999px;
  background: #d8d3c7;
  background-clip: content-box;
}

.vip-page *,
.vip-page *::before,
.vip-page *::after {
  box-sizing: border-box;
}

/* ---------- 进入动画 ---------- */

.vip-page {
  animation: vip-page-fade 0.24s ease-out both;
}

.vip-nav {
  animation: vip-nav-fade 0.3s ease-out both;
}

.vip-hero {
  animation: vip-rise 0.42s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

.vip-plan {
  animation: vip-plan-pop 0.46s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

.vip-plan:nth-child(1) {
  animation-delay: 0.06s;
}

.vip-plan:nth-child(2) {
  animation-delay: 0.13s;
}

.vip-plan:nth-child(3) {
  animation-delay: 0.2s;
}

.vip-footnote {
  animation: vip-rise 0.4s ease-out 0.3s both;
}

@keyframes vip-page-fade {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes vip-nav-fade {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes vip-rise {
  from {
    opacity: 0;
    translate: 0 10px;
  }

  to {
    opacity: 1;
    translate: 0 0;
  }
}

@keyframes vip-plan-pop {
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


/* ---------- 顶部导航 ---------- */

.vip-nav {
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

.vip-brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--vip-ink);
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: 0.01em;
  text-decoration: none;
}

.vip-brand-mark {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border: 1px solid #d3e4da;
  border-radius: 8px;
  background: var(--vip-accent-soft);
  color: var(--vip-accent-strong);
}

.vip-brand-mark svg {
  width: 18px;
  height: 18px;
}

.vip-nav-divider {
  width: 1px;
  height: 16px;
  background: var(--vip-line-strong);
}

.vip-nav-label {
  margin-right: auto;
  color: var(--vip-muted);
  font-size: 12.5px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.vip-back {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 34px;
  padding: 0 12px 0 9px;
  border: 1px solid var(--vip-line);
  border-radius: 9px;
  background: #fff;
  color: var(--vip-ink-soft);
  font: inherit;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}

.vip-back svg {
  width: 16px;
  height: 16px;
}

.vip-back:hover {
  border-color: var(--vip-accent);
  background: var(--vip-accent-soft);
  color: var(--vip-accent-strong);
}

/* ---------- 页面主体 ---------- */

.vip-main {
  width: min(100%, 1080px);
  margin: 0 auto;
  padding: clamp(20px, 3.6vw, 32px) clamp(20px, 4vw, 32px) 24px;
}

.vip-hero {
  max-width: 680px;
  margin: 0 auto clamp(20px, 2.8vw, 30px);
  text-align: center;
}

.vip-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 10px;
  border: 1px solid #d9e5de;
  border-radius: 999px;
  background: rgba(237, 243, 240, 0.8);
  color: var(--vip-accent-strong);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.vip-eyebrow svg {
  width: 12px;
  height: 12px;
}

.vip-title {
  margin: 12px 0 8px;
  color: var(--vip-ink);
  font-size: clamp(27px, 3.4vw, 40px);
  font-weight: 650;
  letter-spacing: -0.03em;
  line-height: 1.22;
  text-wrap: balance;
}

.vip-title em {
  color: var(--vip-accent);
  font-style: normal;
}

.vip-subtitle {
  max-width: 540px;
  margin: 0 auto;
  color: var(--vip-muted);
  font-size: clamp(13px, 1.3vw, 14.5px);
  line-height: 1.65;
  text-wrap: balance;
}

/* ---------- 三档方案 ---------- */

.vip-plans {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(12px, 1.6vw, 18px);
  align-items: stretch;
}

.vip-plan {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: clamp(20px, 2vw, 24px);
  border: 1px solid var(--vip-line);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 1px 2px rgba(35, 40, 36, 0.04);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.vip-plan:hover {
  transform: translateY(-2px);
  border-color: var(--vip-line-strong);
  box-shadow: 0 22px 42px -34px rgba(31, 36, 33, 0.32);
}

.vip-plan--pro {
  border-color: #bcd6c8;
  background:
    radial-gradient(120% 90% at 100% 0%, rgba(47, 107, 87, 0.1) 0%, rgba(47, 107, 87, 0) 58%),
    #f5f9f7;
  box-shadow: 0 18px 38px -32px rgba(47, 107, 87, 0.5);
}

.vip-plan--pro:hover {
  border-color: var(--vip-accent);
  box-shadow: 0 24px 46px -32px rgba(47, 107, 87, 0.55);
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
  color: var(--vip-ink);
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
  border: 1px solid var(--vip-line);
  background: #f8f9f7;
  color: var(--vip-muted);
}

.plan-desc {
  margin: 4px 0 0;
  color: var(--vip-muted);
  font-size: 12px;
  line-height: 1.5;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 2px;
  margin: 16px 0 0;
  color: var(--vip-ink);
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
  color: var(--vip-muted-soft);
  font-size: 12px;
  font-weight: 500;
}

.plan-note {
  margin: 7px 0 0;
  color: var(--vip-muted-soft);
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
  border-top: 1px solid var(--vip-line);
  list-style: none;
}

.vip-plan--pro .plan-features {
  border-top-color: rgba(47, 107, 87, 0.16);
}

.plan-features li {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: var(--vip-ink-soft);
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
  background: var(--vip-accent-soft);
  color: var(--vip-accent);
  font-size: 9.5px;
  font-weight: 700;
  line-height: 1;
}

.vip-plan--pro .plan-features li::before {
  background: #e0eee6;
  color: var(--vip-accent-strong);
}

.plan-btn {
  width: 100%;
  height: 40px;
  margin-top: auto;
  border: 1px solid var(--vip-line-strong);
  border-radius: 10px;
  background: #fff;
  color: var(--vip-ink);
  font: inherit;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease, background 0.15s ease;
}

.plan-btn:hover {
  border-color: var(--vip-accent);
  background: var(--vip-accent-soft);
  color: var(--vip-accent-strong);
}

.vip-plan--pro .plan-btn--primary {
  border-color: #bcd6c8;
  background: #dcebe2;
  color: var(--vip-accent-strong);
}

.vip-plan--pro .plan-btn--primary:hover {
  border-color: var(--vip-accent);
  background: #cfe3d8;
  color: #1d4536;
}

/* ---------- 页脚说明 ---------- */

.vip-footnote {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  margin: 18px 0 0;
  color: var(--vip-muted-soft);
  font-size: 11.5px;
  line-height: 1.6;
  text-align: center;
}

.vip-footnote svg {
  flex: none;
  width: 14px;
  height: 14px;
}

/* ---------- 平板 / 手机 ---------- */

@media (max-width: 900px) {
  .vip-nav {
    height: 52px;
  }

  .vip-main {
    padding-top: 22px;
    padding-bottom: 26px;
  }

  .vip-hero {
    margin-bottom: 18px;
  }

  .vip-plans {
    grid-template-columns: minmax(0, 1fr);
    max-width: 500px;
    margin: 0 auto;
    gap: 12px;
  }

  .vip-plan {
    padding: 20px;
  }

  .vip-plan:hover {
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
  .vip-nav {
    gap: 10px;
    padding: 0 12px;
  }

  .vip-brand {
    margin-right: auto;
    font-size: 13.5px;
  }

  .vip-brand-mark {
    width: 28px;
    height: 28px;
  }

  .vip-brand-mark svg {
    width: 16px;
    height: 16px;
  }

  .vip-nav-divider,
  .vip-nav-label {
    display: none;
  }

  .vip-back {
    gap: 2px;
    padding: 0 9px 0 6px;
  }

  .vip-back span {
    display: none;
  }

  .vip-main {
    padding: 18px 12px 20px;
  }

  .vip-eyebrow {
    display: none;
  }

  .vip-title {
    margin: 0 0 6px;
    font-size: 24px;
    line-height: 1.3;
  }

  .vip-subtitle {
    font-size: 12px;
    line-height: 1.6;
  }

  .vip-hero {
    margin-bottom: 14px;
  }

  .vip-plans {
    gap: 10px;
  }

  .vip-plan {
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

  .vip-footnote {
    align-items: flex-start;
    margin-top: 14px;
    padding: 0 2px;
    font-size: 11px;
    line-height: 1.55;
    text-align: left;
  }
}

@media (prefers-reduced-motion: reduce) {
  .vip-plan,
  .vip-back,
  .plan-btn {
    transition: none;
  }

  .vip-plan:hover {
    transform: none;
  }
}
</style>

<!--
  用法（父组件中）：
  import VipPage from './components/VipPage.vue'

  <VipPage v-if="showVip" @close="showVip = false" />

  建议放在 App.vue 根层级，用 v-if 整页切换；vip-page 自带 100dvh 与滚动。
-->
