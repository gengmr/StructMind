from st_on_hover_tabs import on_hover_tabs
import streamlit as st

st.set_page_config(layout="wide")
st.header("Custom tab component for on-hover navigation bar")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


main_tabs = on_hover_tabs(tabName=['Dashboard', 'Money', 'Economy'],
                              iconName=['dashboard', 'money', 'economy'], default_choice=0)
print(main_tabs)


