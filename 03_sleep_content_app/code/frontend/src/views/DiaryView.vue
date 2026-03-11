<template>
  <div>
    <div class="card">
      <div class="card-title">📝 睡眠日记</div>
      <div class="card-desc">记录今天的状态，生成一份温暖的个性化睡眠日记模板</div>

      <div class="form-grid">
        <div class="form-group">
          <label>今天的心情</label>
          <input v-model="form.mood_today" placeholder="例如：压力大、开心、平静..." />
        </div>
        <div class="form-group">
          <label>身体状态</label>
          <input v-model="form.physical_state" placeholder="例如：很累、精力充沛..." />
        </div>
        <div class="form-group">
          <label>今晚的睡眠目标</label>
          <input v-model="form.sleep_goal" placeholder="例如：早点睡、睡得更深..." />
        </div>
        <div class="form-group">
          <label>今天的特别事情（选填）</label>
          <input v-model="form.special_event" placeholder="例如：完成了重要项目..." />
        </div>
      </div>

      <button class="submit-btn" @click="generate" :disabled="loading || !isValid">
        {{ loading ? '正在生成' : '📝 生成日记模板' }}
        <span v-if="loading" class="loading-dots"></span>
      </button>
      <div v-if="!isValid && submitted" class="error-msg">请填写心情、身体状态和睡眠目标</div>
      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>

    <div v-if="result" class="result-card">
      <div class="result-text">{{ result }}</div>
      <div class="result-actions">
        <button class="action-btn" @click="download">💾 下载日记</button>
        <button class="action-btn" @click="result = ''">✕ 清除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const form = reactive({ mood_today: '', physical_state: '', sleep_goal: '', special_event: '' })
const loading = ref(false)
const result = ref('')
const error = ref('')
const submitted = ref(false)

const isValid = computed(() => form.mood_today && form.physical_state && form.sleep_goal)

async function generate() {
  submitted.value = true
  if (!isValid.value) return
  loading.value = true
  error.value = ''
  result.value = ''
  try {
    const res = await fetch(`${API_BASE}/api/diary`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await res.json()
    result.value = data.content
  } catch (e) {
    error.value = '请求失败，请检查后端服务是否启动'
  } finally {
    loading.value = false
  }
}

function download() {
  const blob = new Blob([result.value], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = '睡眠日记.txt'; a.click()
  URL.revokeObjectURL(url)
}
</script>
