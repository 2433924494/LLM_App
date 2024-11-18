import langchain
from utils import generate_weibo
import streamlit as st
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
with st.sidebar:
    st.session_state.api_key = st.text_input("输入通义千问的API密钥：", type="password")
st.write('# 🎭微博文案小助手')
emotions=['激昂','高兴','伤感','悲壮','自定']
emotion_select=st.selectbox('选择情感:',emotions)
emotion=st.text_input('情感:',value='' if emotion_select=='自定' else emotion_select)
theme=st.text_input('主题:')
if st.button('开始生成'):
    with st.spinner('生成中...'):
        result = generate_weibo(theme, emotion, st.session_state.api_key)
        st.write('### 标签:\n'+result.label+'\n### 文案:\n'+result.text)