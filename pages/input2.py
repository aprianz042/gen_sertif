import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io, os, zipfile
from sidebar import render_sidebar

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

render_sidebar()

st.markdown("<h1 style='text-align:center;'>Generator 2 Field</h1>", unsafe_allow_html=True)

# LOAD FONT
fonts = {}
if os.path.exists("fonts"):
    for f in os.listdir("fonts"):
        if f.endswith(".ttf"):
            fonts[f.replace(".ttf","")] = os.path.join("fonts", f)

col1, col2 = st.columns([1, 1])

# FORM
with col1:
    template_file = st.file_uploader(
    "Template",
    type=["jpg", "jpeg", "png"]
)
    csv_file = st.file_uploader(
    "CSV",
    type=["csv"]
)

    font_name = st.selectbox("Font", list(fonts.keys())) if fonts else None

    font_size1 = st.slider("Font Size Input1", 20, 150, 60)
    font_size2 = st.slider("Font Size Input2", 20, 150, 40)

    color = st.color_picker("Warna", "#000000")

    with st.expander("📍 Posisi Input1", True):
        mode1 = st.selectbox("Posisi Input1", ["Center","Left","Right","Custom"])
        x1 = st.number_input("X Input1", value=100) if mode1=="Custom" else None
        y1 = st.number_input("Y Input1", value=600)

    with st.expander("📍 Posisi Input2", True):
        mode2 = st.selectbox("Posisi Input2", ["Center","Left","Right","Custom"])
        x2 = st.number_input("X Input2", value=100) if mode2=="Custom" else None
        y2 = st.number_input("Y Input2", value=700)

    preview = st.button("Preview")
    generate = st.button("Generate")

# OUTPUT
with col2:
    preview_area = st.container()
    generate_area = st.container()

# PREVIEW
if preview:
    if not template_file or not csv_file:
        preview_area.warning("Upload template & CSV dulu")
    else:
        df = pd.read_csv(csv_file, dtype=str)

        if not {"input1","input2"}.issubset(df.columns):
            preview_area.error("CSV harus punya kolom: input1 & input2")
            st.stop()

        row = df.iloc[0]
        t1, t2 = str(row["input1"]), str(row["input2"])

        image = Image.open(template_file).convert("RGB")
        draw = ImageDraw.Draw(image)

        f1 = ImageFont.truetype(fonts[font_name], font_size1)
        f2 = ImageFont.truetype(fonts[font_name], font_size2)

        w_img, _ = image.size

        # input1
        w1 = draw.textbbox((0,0), t1, font=f1)[2]
        pos1 = (w_img - w1)/2 if mode1=="Center" else (50 if mode1=="Left" else (w_img - w1 - 50 if mode1=="Right" else x1))

        # input2
        w2 = draw.textbbox((0,0), t2, font=f2)[2]
        pos2 = (w_img - w2)/2 if mode2=="Center" else (50 if mode2=="Left" else (w_img - w2 - 50 if mode2=="Right" else x2))

        draw.text((pos1, y1), t1, font=f1, fill=color)
        draw.text((pos2, y2), t2, font=f2, fill=color)

        preview_area.image(image, caption=f"{t1} | {t2}")

# GENERATE
if generate:
    if not template_file or not csv_file:
        generate_area.error("Template & CSV wajib diisi")
    else:
        df = pd.read_csv(csv_file, dtype=str)

        if not {"input1","input2"}.issubset(df.columns):
            generate_area.error("CSV harus punya kolom: input1 & input2")
            st.stop()

        zip_buffer = io.BytesIO()
        z = zipfile.ZipFile(zip_buffer, "w")

        progress = generate_area.progress(0)

        for i,row in df.iterrows():
            t1, t2 = str(row["input1"]), str(row["input2"])

            image = Image.open(template_file).convert("RGB")
            draw = ImageDraw.Draw(image)

            f1 = ImageFont.truetype(fonts[font_name], font_size1)
            f2 = ImageFont.truetype(fonts[font_name], font_size2)

            w_img, _ = image.size

            w1 = draw.textbbox((0,0), t1, font=f1)[2]
            pos1 = (w_img - w1)/2 if mode1=="Center" else (50 if mode1=="Left" else (w_img - w1 - 50 if mode1=="Right" else x1))

            w2 = draw.textbbox((0,0), t2, font=f2)[2]
            pos2 = (w_img - w2)/2 if mode2=="Center" else (50 if mode2=="Left" else (w_img - w2 - 50 if mode2=="Right" else x2))

            draw.text((pos1, y1), t1, font=f1, fill=color)
            draw.text((pos2, y2), t2, font=f2, fill=color)

            pdf = io.BytesIO()
            image.save(pdf, "PDF")

            z.writestr(f"{str(i+1).zfill(3)}_{t1}.pdf", pdf.getvalue())
            progress.progress((i+1)/len(df))

        z.close()

        generate_area.download_button("📦 Download ZIP", zip_buffer.getvalue(), "sertifikat_2field.zip")