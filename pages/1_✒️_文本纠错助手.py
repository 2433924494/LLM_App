import streamlit as st
from Lab1_utils import *
# 确保每个用户都有独立的会话状态存储
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
with st.sidebar:
    st.session_state.api_key = st.text_input("输入通义千问的API密钥：", type="password")

st.write('# ✒️文本纠错助手')
# 添加示例文本及选择功能
example_texts = {
    "示例 1": "为了全面推广利用菜籽饼或棉籽饼喂猪，加速发展养猪事业，这个县举办了三期饲养员技术培训班。",
    "示例 2": "上海文艺出版社会出版的《生存》，作者是一位旅居海外二十多年的加拿大籍华裔作者之手。",
    "示例 3": "有人主张接受，有人反对，他同意这种主张。"
}

selected_example = st.selectbox("选择示例", list(example_texts.keys()))
user_input = st.text_area("请输入需要纠错的文本:", value=example_texts.get(selected_example, ""))

if st.button('开始纠错'):
    st.write('#### 结果：\n')
    st.write_stream(text_correction(user_input, st.session_state.api_key))
