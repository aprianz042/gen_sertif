import streamlit as st
import pandas as pd
import os
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

def load_csv_bytes(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None

# =========================
# LANGSUNG TAMPILKAN (TANPA run())
# =========================

st.title("📘 Panduan Penggunaan Generator Sertifikat")


# =========================
# 1 FIELD
# =========================
st.subheader("🟢 Contoh 1 Field (input1)")
st.image("template/INPUT1.png", caption="Contoh Sertifikat", use_container_width=True)
st.markdown("### 📑 Contoh Format CSV")

df1 = pd.DataFrame({
    "input1": ["Budi Santoso", "Siti Aminah", "Andi Wijaya"]
})

st.dataframe(df1, use_container_width=True)

csv1 = load_csv_bytes("template/input1.csv")
st.download_button("⬇️ Download Template", csv1, "input1.csv")

st.divider()

# =========================
# 2 FIELD
# =========================
st.subheader("🟡 Contoh 2 Field (input1, input2)")
st.image("template/INPUT2.png", caption="Contoh Sertifikat", use_container_width=True)
st.markdown("### 📑 Contoh Format CSV")

df2 = pd.DataFrame({
    "input1": ["Budi Santoso", "Siti Aminah", "Andi Wijaya"],
    "input2": ["1987654321", "1981234567", "1989988776"]
})

st.dataframe(df2, use_container_width=True)

csv2 = load_csv_bytes("template/input2.csv")
st.download_button("⬇️ Download Template", csv2, "input2.csv")

st.divider()

# =========================
# 3 FIELD
# =========================
st.subheader("🔵 Contoh 3 Field (input1, input2, input3)")
st.image("template/INPUT3.png", caption="Contoh Sertifikat", use_container_width=True)
st.markdown("### 📑 Contoh Format CSV")

df3 = pd.DataFrame({
    "input1": ["Budi Santoso", "Siti Aminah", "Andi Wijaya"],
    "input2": ["1987654321", "1981234567", "1989988776"],
    "input3": ["Analis Sistem", "Programmer", "Administrator"]
})

st.dataframe(df3, use_container_width=True)

csv3 = load_csv_bytes("template/input3.csv")
st.download_button("⬇️ Download Template", csv3, "input3.csv")

st.divider()

# =========================
# CATATAN
# =========================
st.markdown("### ⚠️ Catatan Penting")
st.markdown("""
- Gunakan format **CSV UTF-8**
- Jangan ubah nama kolom (input1, input2, input3)
- Data harus dimulai dari baris ke-2
- Tidak boleh ada kolom kosong di header
""")

st.success("Siap digunakan 🚀")