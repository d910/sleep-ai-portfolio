<template>
  <div>
    <div class="card">
      <div class="card-title">🧘 冥想引导</div>
      <div class="card-desc">根据你此刻的状态，生成专属冥想引导词，并转成语音带你放松</div>

      <div class="form-grid">
        <div class="form-group">
          <label>冥想时长</label>
          <select v-model="form.duration">
            <option v-for="d in durations" :key="d" :value="d">{{ d }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>当前情绪</label>
          <select v-model="form.emotion">
            <option v-for="e in emotions" :key="e" :value="e">{{ e }}</option>
          </select>
        </div>
      </div>

      <div class="form-group" style="margin-bottom: 24px;">
        <label>冥想类型</label>
        <div class="radio-group">
          <button
            v-for="t in meditationTypes"
            :key="t"
            :class="['radio-btn', { selected: form.meditation_type === t }]"
            @click="form.meditation_type = t"
          >{{ t }}</button>
        </div>
      </div>

      <div style="display:flex; gap:12px;">
        <button class="submit-btn" @click="generateText" :disabled="loadingText" style="flex:1">
          {{ loadingText ? '生成中' : '📝 生成文字脚本' }}
          <span v-if="loadingText" class="loading-dots"></span>
        </button>
        <button class="submit-btn" @click="generateAudio" :disabled="loadingAudio" style="flex:1; background: linear-gradient(135deg,#6366f1,#8b5cf6)">
          {{ loadingAudio ? '合成中' : '🎧 生成语音' }}
          <span v-if="loadingAudio" class="loading-dots"></span>
        </button>
      </div>
      <div v-if="error" class="error-msg">{{ error }}</div>
    </div>

    <div v-if="scriptResult" class="result-card">
      <div class="result-text">{{ scriptResult }}</div>
      <div class="result-actions">
        <button class="action-btn" @click="downloadText">💾 下载脚本</button>
        <button class="action-btn" @click="scriptResult = ''">✕ 清除</button>
      </div>
    </div>

    <div v-if="audioUrl" class="result-card">
      <div style="color: var(--text-muted); font-size:0.85rem; margin-bottom:12px;">🎧 语音播放</div>
      <audio :src="audioUrl" controls style="width:100%; margin-bottom:12px;"></audio>
      <div class="result-actions">
        <a :href="audioUrl" download="冥想引导.wav" class="action-btn" style="text-decoration:none; display:inline-block;">💾 下载语音</a>
        <button class="action-btn" @click="audioUrl = ''">✕ 清除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

const durations = ['5分钟', '10分钟', '15分钟', '20分钟']
const emotions = ['😰 焦虑紧张', '😊 平静放松', '😔 疲惫劳累', '😤 烦躁不安', '😃 精力充沛']
const meditationTypes = ['呼吸冥想', '身体扫描', '正念冥想', '感恩冥想']

const form = reactive({ duration: '10分钟', emotion: '😔 疲惫劳累', meditation_type: '呼吸冥想' })
const loadingText = ref(false)
const loadingAudio = ref(false)
const scriptResult = ref('')
const audioUrl = ref('')
const error = ref('')

async function generateText() {
  loadingText.value = true
  error.value = ''
  scriptResult.value = ''
  try {
    const res = await fetch(`${API_BASE}/api/meditation`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const data = await res.json()
    scriptResult.value = data.content
  } catch (e) {
    error.value = '请求失败，请检查后端服务是否启动'
  } finally {
    loadingText.value = false
  }
}

async function generateAudio() {
  loadingAudio.value = true
  error.value = ''
  audioUrl.value = ''
  try {
    const res = await fetch(`${API_BASE}/api/meditation/audio`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    const blob = await res.blob()
    audioUrl.value = URL.createObjectURL(blob)
  } catch (e) {
    error.value = '语音生成失败，请检查 API Key 或后端服务'
  } finally {
    loadingAudio.value = false
  }
}

function downloadText() {
  const blob = new Blob([scriptResult.value], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = '冥想脚本.txt'; a.click()
  URL.revokeObjectURL(url)
}
</script>
