import streamlit as st

# 初始化session_state
if 'selected_option' not in st.session_state:
    st.session_state['selected_option'] = '默认选项'

# 定义当选择框值改变时的处理函数
def on_selectbox_change():
    st.session_state['selected_option'] = st.session_state['temp_selected_option']

# 创建selectbox
selected = st.selectbox(
    '选择一个选项',
    options=['选项1', '选项2', '选项3'],
    index=0,
    key='temp_selected_option',
    on_change=on_selectbox_change
)

# 保持选择的值
st.session_state['selected_option'] = selected

# 显示当前选择的值
st.write('你选择了：', st.session_state['selected_option'])
