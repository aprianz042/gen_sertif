import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Generator Sertifikat",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔥 sembunyikan menu default
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

render_sidebar()

st.switch_page("pages/panduan.py")