<template>
  <div id="app">
    <div class="stars"></div>
    <nav class="navbar">
      <div class="nav-logo">🌙 睡前助手</div>
      <div class="nav-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['nav-btn', { active: currentTab === tab.key }]"
          @click="currentTab = tab.key"
        >
          {{ tab.icon }} {{ tab.label }}
        </button>
      </div>
    </nav>

    <main class="main-content">
      <StoryView v-if="currentTab === 'story'" />
      <MeditationView v-if="currentTab === 'meditation'" />
      <DiaryView v-if="currentTab === 'diary'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import StoryView from './views/StoryView.vue'
import MeditationView from './views/MeditationView.vue'
import DiaryView from './views/DiaryView.vue'

const currentTab = ref('story')

const tabs = [
  { key: 'story', icon: '📖', label: '睡前故事' },
  { key: 'meditation', icon: '🧘', label: '冥想引导' },
  { key: 'diary', icon: '📝', label: '睡眠日记' },
]
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600&family=ZCOOL+XiaoWei&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #0a0e1a;
  --surface: #111827;
  --surface2: #1a2235;
  --border: #2a3550;
  --accent: #7c9ef5;
  --accent2: #a78bfa;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --moon: #fde68a;
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Noto Serif SC', serif;
  min-height: 100vh;
}

#app { min-height: 100vh; position: relative; overflow-x: hidden; }

/* 星空背景 */
.stars {
  position: fixed; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(124,158,245,0.08) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(167,139,250,0.08) 0%, transparent 50%);
  pointer-events: none;
}
.stars::before {
  content: '';
  position: absolute; inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 25% 60%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 40% 25%, rgba(255,255,255,0.7) 0%, transparent 100%),
    radial-gradient(1px 1px at 55% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 10%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 85% 45%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 92% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
    radial-gradient(1px 1px at 5% 90%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 60% 50%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 33% 88%, rgba(255,255,255,0.6) 0%, transparent 100%);
}

/* 导航栏 */
.navbar {
  position: relative; z-index: 10;
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 40px;
  background: rgba(17,24,39,0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  font-family: 'ZCOOL XiaoWei', serif;
  font-size: 1.4rem;
  color: var(--moon);
  letter-spacing: 0.05em;
}
.nav-tabs { display: flex; gap: 8px; }
.nav-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Noto Serif SC', serif;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}
.nav-btn:hover { border-color: var(--accent); color: var(--accent); }
.nav-btn.active {
  background: linear-gradient(135deg, rgba(124,158,245,0.2), rgba(167,139,250,0.2));
  border-color: var(--accent);
  color: var(--text);
}

/* 主内容区 */
.main-content {
  position: relative; z-index: 1;
  max-width: 860px;
  margin: 40px auto;
  padding: 0 24px;
}

/* 通用卡片 */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
}
.card-title {
  font-family: 'ZCOOL XiaoWei', serif;
  font-size: 1.5rem;
  color: var(--moon);
  margin-bottom: 8px;
}
.card-desc { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 28px; line-height: 1.7; }

/* 表单元素 */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
.form-group { display: flex; flex-direction: column; gap: 8px; }
.form-group label { color: var(--text-muted); font-size: 0.85rem; }
.form-group select,
.form-group input,
.form-group textarea {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  padding: 10px 14px;
  border-radius: 10px;
  font-family: 'Noto Serif SC', serif;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}
.form-group select:focus,
.form-group input:focus,
.form-group textarea:focus { border-color: var(--accent); }
.form-group textarea { resize: vertical; min-height: 80px; }

/* 单选组 */
.radio-group { display: flex; gap: 10px; flex-wrap: wrap; }
.radio-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
  font-family: 'Noto Serif SC', serif;
}
.radio-btn:hover { border-color: var(--accent); }
.radio-btn.selected { background: rgba(124,158,245,0.15); border-color: var(--accent); color: var(--text); }

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #7c9ef5, #a78bfa);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-family: 'Noto Serif SC', serif;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  letter-spacing: 0.05em;
}
.submit-btn:hover { opacity: 0.9; }
.submit-btn:active { transform: scale(0.99); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* 结果区域 */
.result-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  margin-top: 24px;
}
.result-text {
  color: var(--text);
  line-height: 2;
  font-size: 0.95rem;
  white-space: pre-wrap;
}
.result-actions { display: flex; gap: 10px; margin-top: 16px; }
.action-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-muted);
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-family: 'Noto Serif SC', serif;
  transition: all 0.2s;
}
.action-btn:hover { border-color: var(--accent); color: var(--accent); }

/* 加载状态 */
.loading {
  text-align: center;
  padding: 40px;
  color: var(--text-muted);
}
.loading-dots::after {
  content: '';
  animation: dots 1.5s infinite;
}
@keyframes dots {
  0%,20% { content: ''; }
  40% { content: '.'; }
  60% { content: '..'; }
  80%,100% { content: '...'; }
}

/* 错误提示 */
.error-msg {
  color: #f87171;
  font-size: 0.85rem;
  margin-top: 12px;
  padding: 10px 14px;
  background: rgba(248,113,113,0.1);
  border-radius: 8px;
  border: 1px solid rgba(248,113,113,0.3);
}

@media (max-width: 600px) {
  .navbar { flex-direction: column; gap: 12px; padding: 16px 20px; }
  .form-grid { grid-template-columns: 1fr; }
  .main-content { margin: 20px auto; }
  .card { padding: 20px; }
}
</style>
