import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to BIDGPT! 👋")
st.sidebar.success("请选择以上BIDGPT模块")
st.markdown(
    """
    欢迎使用华鑫公司人工智能标书工具 BIDGPT V1.0
"""
)