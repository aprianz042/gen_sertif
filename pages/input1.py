import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io, os, zipfile
from sidebar import render_sidebar

render_sidebar()

st.set_page_config(
    page_title="Generator Sertifikat",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔥 sembunyikan menu default
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>Generator 1 Field</h1>", unsafe_allow_html=True)

# =========================
# LOAD FONT
# =========================
fonts = {}
if os.path.exists("fonts"):
    for f in os.listdir("fonts"):
        if f.endswith(".ttf"):
            fonts[f.replace(".ttf","")] = os.path.join("fonts", f)

col1, col2 = st.columns([1, 1])

# =========================
# FORM
# =========================
with col1:
    template_file = st.file_uploader("Template")
    csv_file = st.file_uploader("CSV")

    font_name = st.selectbox("Font", list(fonts.keys())) if fonts else None
    font_size = st.slider("Font Size Input1", 20, 150, 60)

    color = st.color_picker("Warna", "#000000")

    with st.expander("📍 Posisi Input1", True):
        mode = st.selectbox("Posisi", ["Center","Left","Right","Custom"])
        x = st.number_input("X Input1", value=100) if mode=="Custom" else None
        y = st.number_input("Y Input1", value=600)

    preview = st.button("Preview")
    generate = st.button("Generate")

# =========================
# OUTPUT
# =========================
with col2:
    preview_area = st.container()
    generate_area = st.container()

# =========================
# PREVIEW
# =========================
if preview:
    if not template_file or not csv_file:
        preview_area.warning("Upload template & CSV dulu")
    else:
        df = pd.read_csv(csv_file, dtype=str)

        if "input1" not in df.columns:
            preview_area.error("CSV harus punya kolom: input1")
            st.stop()

        text_val = str(df.iloc[0]["input1"])

        image = Image.open(template_file).convert("RGB")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(fonts[font_name], font_size)

        image_width, _ = image.size
        bbox = draw.textbbox((0,0), text_val, font=font)
        text_width = bbox[2] - bbox[0]

        if mode == "Center":
            x_pos = (image_width - text_width)/2
        elif mode == "Left":
            x_pos = 50
        elif mode == "Right":
            x_pos = image_width - text_width - 50
        else:
            x_pos = x

        draw.text((x_pos, y), text_val, font=font, fill=color)

        preview_area.image(image, caption=text_val)

# =========================
# GENERATE
# =========================
if generate:
    if not template_file or not csv_file:
        generate_area.error("Template & CSV wajib diisi")
    else:
        df = pd.read_csv(csv_file, dtype=str)

        if "input1" not in df.columns:
            generate_area.error("CSV harus punya kolom: input1")
            st.stop()

        zip_buffer = io.BytesIO()
        z = zipfile.ZipFile(zip_buffer, "w")

        progress = generate_area.progress(0)
        status = generate_area.empty()

        for i,row in df.iterrows():
            text_val = str(row["input1"])

            image = Image.open(template_file).convert("RGB")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(fonts[font_name], font_size)

            image_width, _ = image.size
            bbox = draw.textbbox((0,0), text_val, font=font)
            text_width = bbox[2] - bbox[0]

            if mode == "Center":
                x_pos = (image_width - text_width)/2
            elif mode == "Left":
                x_pos = 50
            elif mode == "Right":
                x_pos = image_width - text_width - 50
            else:
                x_pos = x

            draw.text((x_pos, y), text_val, font=font, fill=color)

            pdf = io.BytesIO()
            image.save(pdf, "PDF")

            filename = f"{str(i+1).zfill(3)}_{text_val.replace(' ','_')}.pdf"
            z.writestr(filename, pdf.getvalue())

            progress.progress((i+1)/len(df))
            status.text(f"Memproses: {text_val}")

        z.close()

        generate_area.success(f"Selesai generate {len(df)} sertifikat")

        generate_area.download_button(
            "📦 Download ZIP",
            zip_buffer.getvalue(),
            "sertifikat_1field.zip"
        )