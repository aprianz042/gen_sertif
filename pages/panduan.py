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
# Template
# =========================
st.subheader("### Persiapan Template")
st.markdown("Siapkan template yang ingin di-generate, contoh : ")

dataf = pd.DataFrame({
    "nama": ["Budi Santoso", "Siti Aminah", "Andi Wijaya"],
    "no id": ["1987654321", "1981234567", "1989988776"],
    "jabatan": ["Analis Sistem", "Programmer", "Administrator"],
    "instansi": ["Pemkab XXX", "Pemprov XXX", "Kementerian XXX"]
})

st.dataframe(dataf, use_container_width=True)
st.markdown("nama / no id / jabatan / instansi bebas diganti dengan nama kolom apapun. Contoh template data dapat diunduh pada link di bawah")

csv3 = load_csv_bytes("template/input3.csv")
st.download_button("⬇️ Download Template", csv3, "input3.csv")

st.divider()

# =========================
# 3 FIELD
# =========================
st.subheader("### Siapkan template sertifikat kosong (tanpa data peserta), contoh :")
st.image("template/kosong.png")
st.divider()

# =========================
# CATATAN
# =========================
st.subheader("🔵 Panduan Penggunaan Aplikasi")

st.success("Upload template sertifikat pada form input berikut")
st.image("template/input_template.png")

st.success("Untuk BULK DATA, upload data csv pada form input berikut")
st.image("template/input_data.png")

st.success("Untuk SINGLE DATA, tambahkan parameter dengan menekan tombol berikut")
st.image("template/tombol_input.png")

st.success("Pilih font dan warna font")
st.image("template/pilih_font.png")

st.success("Atur parameter text sesuai dengan jumlah header data pada Bulk Data atau jumlah input pada Single Data")
st.image("template/param_font.png")

st.success("Klik preview untuk mereview sertifikat, dan klik tombol generate untuk memproses sertifikat")
st.image("template/tombol.png")

st.success("Jika SINGLE DATA maka output-nya hanya 1 pdf, namun jika BULK DATA maka output-nya akan menjadi file ZIP")
st.image("template/download_img.png")
st.image("template/zip_img.png")

