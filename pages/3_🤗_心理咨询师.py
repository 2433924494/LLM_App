import streamlit as st
from Lab3_utils import get_chat_response

st.title('🤗心理咨询师')
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
with st.sidebar:
    st.session_state.api_key = st.text_input("输入通义千问的API密钥：", type="password")
with st.sidebar:
    st.session_state.user_name = st.text_input("输入用户名:", type="default")
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": '我是一名资深心理咨询师,和我对话吧!'}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        res = get_chat_response(user_input=prompt, user_name=st.session_state.user_name, api_key=st.session_state.api_key)
        text=st.write_stream(res)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": text})
