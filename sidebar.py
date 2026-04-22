import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("## 📂 Menu")

        st.page_link("pages/panduan.py", label="📘 Panduan")
        
        st.page_link("pages/input1.py", label="🟢 Generator 1 Field")
        st.page_link("pages/input2.py", label="🟡 Generator 2 Field")
        st.page_link("pages/input3.py", label="🔵 Generator 3 Field")
        