import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## 📂 Menu")

        st.page_link("pages/panduan.py", label="📘 Panduan")
        st.page_link("pages/dynamic_field.py", label="📥 Bulk Data")
        st.page_link("pages/single.py", label="🎯 Single Data")
        