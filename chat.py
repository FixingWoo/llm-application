import streamlit as st
import time

from dotenv import load_dotenv
from llm import get_ai_response

st.set_page_config(page_title="복무규정 챗봇", page_icon="🤖")

st.title("🤖 복무규정 챗봇")
st.caption("복무규정에 관련된 모든 것을 답해드립니다!")

load_dotenv()

if 'message_list' not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if user_question := st.chat_input(placeholder="복무규정에 관련된 궁금한 내용들을 말씀해주세요!"):
    with st.chat_message("user"):
        start_time = time.time()
        st.write(user_question)
    st.session_state.message_list.append({"role": "user", "content": user_question})

    with st.spinner("답변을 생성하는 중 입니다."):
        ai_response_stream = get_ai_response(user_question)

        ai_message = ""

        with st.chat_message("ai"):
            message_placeholder = st.empty()
            for chunk in ai_response_stream:
                ai_message += chunk
                message_placeholder.write(ai_message)

        end_time = time.time()
        elapsed_time = end_time - start_time
        
        ai_message_with_time = f"{ai_message} <span style='font-size: 14px; color: rgba(0, 0, 0, 0.8);'>({elapsed_time:.2f}초)</span>"
        message_placeholder.markdown(ai_message_with_time, unsafe_allow_html=True)

        # 세션에 메시지 추가
        st.session_state.message_list.append({"role": "ai", "content": ai_message_with_time})
