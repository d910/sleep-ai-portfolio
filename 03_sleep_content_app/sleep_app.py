#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
睡前内容生成器 - Streamlit Web应用
功能：睡前故事生成 + 冥想引导脚本（带语音）+ 睡眠日记模板
"""

import streamlit as st
import dashscope
from dashscope import Generation
from dashscope.audio.tts_v2 import SpeechSynthesizer

# ===== 配置区域 =====
try:
    API_KEY = st.secrets["API_KEY"]
except:
    API_KEY = 'your-api-key-here'

# 设置API Key
dashscope.api_key = API_KEY

# ===== 页面配置 =====
st.set_page_config(
    page_title="睡前内容生成器",
    page_icon="🌙",
    layout="wide"
)

# ===== 辅助函数 =====

def call_ai(prompt, temperature=0.8):
    """
    调用通义千问API生成内容
    
    参数:
        prompt: 提示词
        temperature: 温度参数（创意度）
    
    返回:
        生成的文本
    """
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


# ===== 文字转语音 =====
def text_to_speech(text):
    """
    调用阿里云TTS API将文字转成语音
    
    参数:
        text: 要转换的文字
    
    返回:
        成功: 音频文件的二进制数据
        失败: None
    """
    try:
        # 创建语音合成器
        synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',  
            voice='longxiaochun'  
        )
        
        # 调用语音合成
        audio_data = synthesizer.call(text)
        
        # 返回音频二进制数据
        return audio_data
        
    except Exception as e:
        # 如果出错，返回None，并打印错误信息
        st.error(f"语音生成失败：{str(e)}")
        return None


# ===== 页面标题 =====
st.title("🌙 睡前内容生成器")
st.markdown("---")
st.write("欢迎使用睡前内容生成器！选择下面的功能，帮你准备一个美好的睡眠夜晚 💤")

# ===== 功能选择 =====
tab1, tab2, tab3 = st.tabs(["📖 睡前故事生成", "🧘 冥想引导脚本（带语音）", "📝 睡眠日记模板"])

# ═════════════════════════════════════════════════════════════════
# 功能1：睡前故事生成
# ═════════════════════════════════════════════════════════════════
with tab1:
    st.header("📖 睡前故事生成")
    st.write("选择一个主题，AI会为你创作一个原创的睡前故事~")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 主题选择
        theme = st.selectbox(
            "选择故事主题",
            ["🌲 森林", "⭐ 星空", "🌊 海洋", "🏔️ 山谷", "🌸 花园", "❄️ 雪地"]
        )
        
        # 故事长度
        length = st.select_slider(
            "故事长度",
            options=["短（3分钟）", "中（5分钟）", "长（8分钟）"],
            value="中（5分钟）"
        )
    
    with col2:
        # 故事风格
        style = st.radio(
            "故事风格",
            ["温馨治愈", "奇幻冒险", "平静舒缓"]
        )
    
    # 生成按钮
    if st.button("✨ 生成睡前故事", key="story_btn"):
        with st.spinner("正在创作故事..."):
            # 构建提示词
            length_map = {
                "短（3分钟）": "300字左右",
                "中（5分钟）": "500字左右",
                "长（8分钟）": "800字左右"
            }
            
            prompt = f"""
请创作一个睡前故事。

要求：
- 主题：{theme}
- 风格：{style}
- 长度：{length_map[length]}
- 语言要温柔、舒缓，适合睡前阅读
- 结局要平静、美好，让人心情放松
- 不要有紧张刺激的情节

请直接输出故事内容，不要前言和后语。
"""
            # 调用AI生成（temperature=0.8，比较有创意）
            story = call_ai(prompt, temperature=0.8)
            
            # 显示结果
            st.success("✅ 故事生成完成！")
            st.markdown("### 你的睡前故事")
            st.write(story)
            
            # 下载按钮
            st.download_button(
                label="💾 下载故事",
                data=story,
                file_name="睡前故事.txt",
                mime="text/plain"
            )

# ═════════════════════════════════════════════════════════════════
# 功能2：冥想引导脚本（新增语音功能）
# ═════════════════════════════════════════════════════════════════
with tab2:
    st.header("🧘 冥想引导脚本（带语音）")
    st.write("生成适合你当前状态的冥想引导词，并转成语音播放")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 时长选择
        duration = st.selectbox(
            "冥想时长",
            ["5分钟", "10分钟", "15分钟", "20分钟"]
        )
        
        # 情绪选择
        emotion = st.selectbox(
            "当前情绪",
            ["😰 焦虑紧张", "😊 平静放松", "😔 疲惫劳累", "😤 烦躁不安", "😃 精力充沛"]
        )
    
    with col2:
        # 冥想类型
        meditation_type = st.radio(
            "冥想类型",
            ["呼吸冥想", "身体扫描", "正念冥想", "感恩冥想"]
        )
    
    # 生成按钮
    if st.button("🧘 生成冥想引导（文字+语音）", key="meditation_btn"):
        # ===== 步骤1：生成文字脚本 =====
        with st.spinner("正在生成冥想引导词..."):
            # 构建提示词
            prompt = f"""
请生成一段冥想引导脚本。

要求：
- 时长：{duration}
- 当前情绪：{emotion}
- 冥想类型：{meditation_type}
- 语言要温柔、缓慢，适合跟随引导
- 包含清晰的步骤和时间节点
- 帮助用户从当前情绪状态逐渐进入平静

格式：
1. 开场引导（让用户找到舒适姿势）
2. 主体引导（根据冥想类型设计具体步骤）
3. 结束引导（慢慢回到当下）

请直接输出引导脚本，不要前言和后语，不要输出与内容无关的内容，比如“开场引导、主体引导、结束引导”，以及时间，只输出引导内容。
"""
            # 调用AI生成文字
            meditation_script = call_ai(prompt, temperature=0.6)
            
            # 显示文字结果
            st.success("✅ 冥想脚本生成完成！")
            st.markdown("### 📝 你的冥想引导文字")
            st.info("💡 建议：找一个安静的地方，跟随引导词慢慢练习")
            st.write(meditation_script)
            
            # 下载文字按钮
            st.download_button(
                label="💾 下载文字脚本",
                data=meditation_script,
                file_name="冥想引导脚本.txt",
                mime="text/plain",
                key="download_text"
            )
        
        # ===== 步骤2：转成语音 =====
        st.markdown("---")
        with st.spinner("正在生成语音，请稍候..."):
            # 调用TTS函数
            audio_data = text_to_speech(meditation_script)
            
            # 检查是否成功生成语音
            if audio_data:
                st.success("✅ 语音生成完成！")
                st.markdown("### 🎧 语音播放")
                
                # 播放音频
                # st.audio()接受二进制数据，直接传入audio_data即可
                st.audio(audio_data, format='audio/wav')
                
                # 下载语音按钮
                st.download_button(
                    label="💾 下载语音文件",
                    data=audio_data,
                    file_name="冥想引导.wav",
                    mime="audio/wav",
                    key="download_audio"
                )
                
                # 使用提示
                st.info("""
                💡 **使用建议：**
                - 戴上耳机，音量调到舒适的程度
                - 找一个安静、舒适的地方
                - 闭上眼睛，跟随引导语放松
                - 如果中途走神，温柔地把注意力带回来
                """)
            else:
                # 如果语音生成失败，显示提示
                st.warning("⚠️ 语音生成失败，但你仍然可以阅读或下载文字脚本。")

# ═════════════════════════════════════════════════════════════════
# 功能3：睡眠日记模板
# ═════════════════════════════════════════════════════════════════
with tab3:
    st.header("📝 睡眠日记模板")
    st.write("根据你今天的状态，生成一个个性化的睡眠日记模板")
    
    # 今日状态输入
    st.subheader("📋 今日状态记录")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 情绪状态
        mood_today = st.text_input(
            "今天的心情如何？",
            placeholder="例如：压力大、开心、平静、疲倦..."
        )
        
        # 身体状态
        physical_state = st.text_input(
            "身体状态如何？",
            placeholder="例如：很累、精力充沛、有点头疼..."
        )
    
    with col2:
        # 睡眠目标
        sleep_goal = st.text_input(
            "今晚的睡眠目标是什么？",
            placeholder="例如：早点睡、睡得更深、不做噩梦..."
        )
        
        # 特殊事件
        special_event = st.text_area(
            "今天有什么特别的事情吗？（可选）",
            placeholder="例如：今天完成了一个重要项目、和朋友吵架了...",
            height=80
        )
    
    # 生成按钮
    if st.button("📝 生成日记模板", key="diary_btn"):
        # 检查必填项
        if not mood_today or not physical_state or not sleep_goal:
            st.warning("⚠️ 请至少填写心情、身体状态和睡眠目标")
        else:
            with st.spinner("正在生成个性化日记模板..."):
                # 构建提示词
                prompt = f"""
请根据用户今天的状态，生成一个个性化的睡眠日记模板。

用户今日状态：
- 心情：{mood_today}
- 身体：{physical_state}
- 睡眠目标：{sleep_goal}
- 特殊事件：{special_event if special_event else "无"}

要求：
1. 根据用户状态，给出温暖的回应和建议
2. 生成一个结构化的日记模板，包括：
   - 今日回顾（针对用户提到的状态）
   - 睡前感受（引导用户记录）
   - 明天期待（正向引导）
   - 睡眠计划（具体的助眠行动）
3. 语气温柔、鼓励
4. 适合用户填写和记录

请直接输出日记模板，不要前言和后语。
"""
                # 调用AI生成
                diary_template = call_ai(prompt, temperature=0.7)
                
                # 显示结果
                st.success("✅ 日记模板生成完成！")
                st.markdown("### 你的睡眠日记")
                st.write(diary_template)
                
                # 下载按钮
                st.download_button(
                    label="💾 下载日记模板",
                    data=diary_template,
                    file_name="睡眠日记.txt",
                    mime="text/plain"
                )

# ═════════════════════════════════════════════════════════════════
# 页面底部
# ═════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
    💤 睡前内容生成器 | 基于通义千问API + Streamlit + 语音合成<br>
    祝你今晚睡个好觉 🌙
    </div>
    """,
    unsafe_allow_html=True
)

# ═════════════════════════════════════════════════════════════════
# API Key检查提示
# ═════════════════════════════════════════════════════════════════
if API_KEY == 'your-api-key-here':
    st.error("""
    ⚠️ 请先设置你的API Key！
    
    1. 打开这个文件 sleep_app.py
    2. 找到第13行的 API_KEY = 'your-api-key-here'
    3. 把 'your-api-key-here' 替换成你的通义千问API Key
    4. 保存文件后重新运行
    """)
