<template>
  <div>
    <div class="card">
      <div class="card-title">📖 睡前故事</div>
      <div class="card-desc">选择一个主题，为你创作一个让心灵平静的原创睡前故事</div>

      <div class="form-grid">
        <div class="form-group">
          <label>故事主题</label>
          <select v-model="form.theme">
            <option v-for="t in themes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>故事长度</label>
          <select v-model="form.length">
            <option v-for="l in lengths" :key="l" :value="l">{{ l }}</option>
          </select>
        </div>
      </div>

      <div class="form-group" style="margin-bottom: 24px;">
        <label>故事风格</label>
        <div class="radio-group">
          <button
            v-for="s in styles"
            :key="s"
            :class="['radio-btn', { selected: form.style === s }]"
            @click="form.style = s"
          >{{ s }}</button>
        </div>
      </div>

      <button class="submit-btn" @click="generate" :disabled="loading">
        {{ loading ? '正在创作中' : '✨ 生成睡前故事' }}
        <span v-if="loading" class="loading-dots"></span>
      </button>
      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>

    <div v-if="result" class="result-card">
      <div class="result-text">{{ result }}</div>
      <div class="result-actions">
        <button class="action-btn" @click="download">💾 下载故事</button>
        <button class="action-btn" @click="result = ''">✕ 清除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const themes = ['🌲 森林', '⭐ 星空', '🌊 海洋', '🏔️ 山谷', '🌸 花园', '❄️ 雪地']
const lengths = ['短（3分钟）', '中（5分钟）', '长（8分钟）']
const styles = ['温馨治愈', '奇幻冒险', '平静舒缓']

const form = reactive({ theme: '🌲 森林', length: '中（5分钟）', style: '温馨治愈' })
const loading = ref(false)
const result = ref('')
const error = ref('')

async function generate() {
  loading.value = true
  error.value = ''
  result.value = ''
  try {
    const res = await fetch(`${API_BASE}/api/story`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await res.json()
    result.value = data.content
  } catch (e) {
    error.value = '请求失败，请检查网络或后端服务是否启动'
  } finally {
    loading.value = false
  }
}

function download() {
  const blob = new Blob([result.value], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = '睡前故事.txt'; a.click()
  URL.revokeObjectURL(url)
}
</script>
