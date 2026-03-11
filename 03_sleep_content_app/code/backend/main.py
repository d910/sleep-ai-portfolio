#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import dashscope
from dashscope import Generation
from dashscope.audio.tts_v2 import SpeechSynthesizer
from fastapi.responses import Response
import os

# ===== 初始化 FastAPI 应用 =====
app = FastAPI(title="睡前内容生成器 API", version="1.0.0")

# ===== 配置 CORS（允许前端访问后端）=====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== 配置通义千问 API Key =====
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY", "sk-71d259628cb34d6684789e5e312c0460")

# ===== 定义请求数据结构 =====

class StoryRequest(BaseModel):
    theme: str
    style: str
    length: str

class MeditationRequest(BaseModel):
    duration: str
    emotion: str
    meditation_type: str

class DiaryRequest(BaseModel):
    mood_today: str
    physical_state: str
    sleep_goal: str
    special_event: Optional[str] = ""

# ===== 辅助函数：调用通义千问 =====

def call_ai(prompt: str, temperature: float = 0.8) -> str:
    try:
        response = Generation.call(
            model='qwen-turbo',
            messages=[
                {'role': 'system', 'content': '你是一个温柔专业的睡眠内容创作者。'},
                {'role': 'user', 'content': prompt}
            ],
            result_format='message',
            temperature=temperature,
        )
        if response.status_code == 200:
            return response.output.choices[0].message.content
        else:
            return f"生成失败，错误码：{response.status_code}"
    except Exception as e:
        return f"发生错误：{str(e)}"

# ===== 接口1：生成睡前故事 =====

@app.post("/api/story")
def generate_story(req: StoryRequest):
    length_map = {
        "短（3分钟）": "300字左右",
        "中（5分钟）": "500字左右",
        "长（8分钟）": "800字左右"
    }
    word_count = length_map.get(req.length, "500字左右")

    prompt = f"""
请创作一个睡前故事。
要求：
- 主题：{req.theme}
- 风格：{req.style}
- 长度：{word_count}
- 语言要温柔、舒缓，适合睡前阅读
- 结局要平静、美好，让人心情放松
- 不要有紧张刺激的情节
请直接输出故事内容，不要前言和后语。
"""
    content = call_ai(prompt, temperature=0.8)
    return {"content": content}

# ===== 接口2：生成冥想脚本 =====

@app.post("/api/meditation")
def generate_meditation(req: MeditationRequest):
    prompt = f"""
请生成一段冥想引导脚本。
要求：
- 时长：{req.duration}
- 当前情绪：{req.emotion}
- 冥想类型：{req.meditation_type}
- 语言要温柔、缓慢，适合跟随引导
- 包含清晰的步骤
- 帮助用户从当前情绪状态逐渐进入平静
请直接输出引导脚本，不要前言和后语，不要输出标题或时间标注，只输出引导内容。
"""
    content = call_ai(prompt, temperature=0.6)
    return {"content": content}

# ===== 接口3：生成冥想语音 =====

@app.post("/api/meditation/audio")
def generate_meditation_audio(req: MeditationRequest):
    # 先生成文字
    prompt = f"""
请生成一段冥想引导脚本。
要求：
- 时长：{req.duration}
- 当前情绪：{req.emotion}
- 冥想类型：{req.meditation_type}
- 语言要温柔、缓慢，适合跟随引导
请直接输出引导脚本，不要前言和后语，只输出引导内容。
"""
    script = call_ai(prompt, temperature=0.6)

    # 再转语音
    try:
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',
            voice='longxiaochun'
        )
        audio_data = synthesizer.call(script)
        return Response(content=audio_data, media_type="audio/wav")
    except Exception as e:
        return {"error": f"语音生成失败：{str(e)}"}

# ===== 接口4：生成睡眠日记 =====

@app.post("/api/diary")
def generate_diary(req: DiaryRequest):
    prompt = f"""
请根据用户今天的状态，生成一个个性化的睡眠日记模板。
用户今日状态：
- 心情：{req.mood_today}
- 身体：{req.physical_state}
- 睡眠目标：{req.sleep_goal}
- 特殊事件：{req.special_event if req.special_event else "无"}
要求：
1. 根据用户状态，给出温暖的回应和建议
2. 生成一个结构化的日记模板，包括今日回顾、睡前感受、明天期待、睡眠计划
3. 语气温柔、鼓励
请直接输出日记模板，不要前言和后语。
"""
    content = call_ai(prompt, temperature=0.7)
    return {"content": content}

# ===== 健康检查接口（部署后用来验证服务是否正常）=====

@app.get("/")
def root():
    return {"status": "ok", "message": "睡前内容生成器 API 运行中"}
