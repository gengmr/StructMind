# -*- coding: utf-8 -*-
import streamlit as st

# 初始化session_state
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ''

# 更新函数
def update_text():
    st.session_state['input_text'] = st.session_state["input_box"]
    # 显示实时文本
    st.write("实时显示：", st.session_state['input_text'])

# 文本输入框
text_input = st.text_input("在此输入文本：", value=st.session_state['input_text'], key="input_box", on_change=update_text)


