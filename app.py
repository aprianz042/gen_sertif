import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io
import os
import zipfile

st.set_page_config(page_title="Generator Sertifikat", layout="centered")

st.title("🎓 Generator Sertifikat Otomatis")

# =========================
# AUTO LOAD FONT
# =========================
font_dir = "fonts"

def load_fonts(folder):
    fonts = {}
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.lower().endswith(".ttf"):
                name = file.replace(".ttf", "")
                fonts[name] = os.path.join(folder, file)
    return dict(sorted(fonts.items()))

available_fonts = load_fonts(font_dir)

# =========================
# INPUT
# =========================
template_file = st.file_uploader("📄 Upload Template (PNG/JPG)", type=["png", "jpg", "jpeg"])
csv_file = st.file_uploader("📑 Upload CSV Nama", type=["csv"])

if available_fonts:
    selected_font_name = st.selectbox("🔤 Pilih Font", list(available_fonts.keys()))
else:
    st.warning("⚠️ Tidak ada font di folder /fonts")
    selected_font_name = None

font_size = st.slider("🔠 Ukuran Font", 20, 150, 60)
text_y = st.number_input("📍 Posisi Y Nama", min_value=0, value=600)
text_color = st.color_picker("🎨 Warna Teks", "#000000")

# Tombol
col1, col2 = st.columns(2)

with col1:
    preview_btn = st.button("👀 Preview")

with col2:
    generate_btn = st.button("🚀 Generate Sertifikat")

# =========================
# PREVIEW
# =========================
if preview_btn:
    if not template_file or not csv_file:
        st.error("Template dan CSV wajib diisi!")
    elif not available_fonts:
        st.error("Tambahkan font ke folder /fonts terlebih dahulu!")
    else:
        try:
            df = pd.read_csv(csv_file)

            if "nama" not in df.columns:
                st.error("CSV harus punya kolom 'nama'")
                st.stop()

            # ambil data pertama
            nama = str(df.iloc[0]["nama"])

            font_path = available_fonts[selected_font_name]
            font = ImageFont.truetype(font_path, font_size)

            image = Image.open(template_file).convert("RGB")
            draw = ImageDraw.Draw(image)

            image_width, _ = image.size

            # center horizontal
            bbox = draw.textbbox((0, 0), nama, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (image_width - text_width) / 2

            # gambar teks
            draw.text((text_x, text_y), nama, font=font, fill=text_color)

            st.success("Preview berhasil!")

            # tampilkan preview
            st.image(image, caption=f"Preview: {nama}")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# GENERATE ZIP
# =========================
if generate_btn:
    if not template_file or not csv_file:
        st.error("Template dan CSV wajib diisi!")
    elif not available_fonts:
        st.error("Tambahkan font ke folder /fonts terlebih dahulu!")
    else:
        try:
            df = pd.read_csv(csv_file)

            if "nama" not in df.columns:
                st.error("CSV harus punya kolom 'nama'")
                st.stop()

            font_path = available_fonts[selected_font_name]
            font = ImageFont.truetype(font_path, font_size)

            zip_buffer = io.BytesIO()
            zip_file = zipfile.ZipFile(zip_buffer, "w")

            progress = st.progress(0)

            for i, row in df.iterrows():
                nama = str(row["nama"])

                image = Image.open(template_file).convert("RGB")
                draw = ImageDraw.Draw(image)

                image_width, _ = image.size

                # center horizontal
                bbox = draw.textbbox((0, 0), nama, font=font)
                text_width = bbox[2] - bbox[0]
                text_x = (image_width - text_width) / 2

                # gambar teks
                draw.text((text_x, text_y), nama, font=font, fill=text_color)

                # simpan PDF ke memory
                pdf_bytes = io.BytesIO()
                image.save(pdf_bytes, format="PDF")

                # nama file aman
                safe_name = nama.replace(" ", "_")
                filename = f"{str(i+1).zfill(3)}_{safe_name}.pdf"

                zip_file.writestr(filename, pdf_bytes.getvalue())

                progress.progress((i + 1) / len(df))

            zip_file.close()

            st.success(f"✅ Berhasil generate {len(df)} sertifikat!")

            st.download_button(
                label="📦 Download ZIP",
                data=zip_buffer.getvalue(),
                file_name="sertifikat.zip",
                mime="application/zip"
            )

        except Exception as e:
            st.error(f"Error: {e}")