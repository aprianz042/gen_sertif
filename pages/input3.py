import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io, os, zipfile
from sidebar import render_sidebar

st.set_page_config(
    page_title="Generator Sertifikat",
    page_icon="favicon.png",
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

st.markdown("<h1 style='text-align:center;'>Generator 3 Field</h1>", unsafe_allow_html=True)

fonts = {}
if os.path.exists("fonts"):
    for f in os.listdir("fonts"):
        if f.endswith(".ttf"):
            fonts[f.replace(".ttf","")] = os.path.join("fonts", f)

col1, col2 = st.columns([1, 1])

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

    size1 = st.slider("Font Input1", 20,150,60)
    size2 = st.slider("Font Input2", 20,150,40)
    size3 = st.slider("Font Input3", 20,150,40)

    color = st.color_picker("Warna", "#000000")

    def pos(label, default_y):
        with st.expander(label, True):
            mode = st.selectbox(label, ["Center","Left","Right","Custom"], key=label)
            x = st.number_input(f"X {label}", value=100, key=label+"x") if mode=="Custom" else None
            y = st.number_input(f"Y {label}", value=default_y, key=label+"y")
        return mode, x, y

    m1,x1,y1 = pos("Input1",600)
    m2,x2,y2 = pos("Input2",700)
    m3,x3,y3 = pos("Input3",800)

    preview = st.button("Preview")
    generate = st.button("Generate")

with col2:
    preview_area = st.container()
    generate_area = st.container()

def get_x(mode, x, w_img, w_text):
    if mode=="Center": return (w_img-w_text)/2
    if mode=="Left": return 50
    if mode=="Right": return w_img-w_text-50
    return x

if preview:
    df = pd.read_csv(csv_file, dtype=str)
    r = df.iloc[0]

    t1,t2,t3 = str(r["input1"]),str(r["input2"]),str(r["input3"])

    img = Image.open(template_file).convert("RGB")
    d = ImageDraw.Draw(img)

    f1 = ImageFont.truetype(fonts[font_name], size1)
    f2 = ImageFont.truetype(fonts[font_name], size2)
    f3 = ImageFont.truetype(fonts[font_name], size3)

    w,_ = img.size

    d.text((get_x(m1,x1,w,d.textbbox((0,0),t1,font=f1)[2]), y1), t1, font=f1, fill=color)
    d.text((get_x(m2,x2,w,d.textbbox((0,0),t2,font=f2)[2]), y2), t2, font=f2, fill=color)
    d.text((get_x(m3,x3,w,d.textbbox((0,0),t3,font=f3)[2]), y3), t3, font=f3, fill=color)

    preview_area.image(img)

if generate:
    df = pd.read_csv(csv_file, dtype=str)
    zip_buffer = io.BytesIO()
    z = zipfile.ZipFile(zip_buffer,"w")

    prog = generate_area.progress(0)

    for i,row in df.iterrows():
        img = Image.open(template_file).convert("RGB")
        d = ImageDraw.Draw(img)

        t1,t2,t3 = str(row["input1"]),str(row["input2"]),str(row["input3"])

        f1 = ImageFont.truetype(fonts[font_name], size1)
        f2 = ImageFont.truetype(fonts[font_name], size2)
        f3 = ImageFont.truetype(fonts[font_name], size3)

        w,_ = img.size

        d.text((get_x(m1,x1,w,d.textbbox((0,0),t1,font=f1)[2]), y1), t1, font=f1, fill=color)
        d.text((get_x(m2,x2,w,d.textbbox((0,0),t2,font=f2)[2]), y2), t2, font=f2, fill=color)
        d.text((get_x(m3,x3,w,d.textbbox((0,0),t3,font=f3)[2]), y3), t3, font=f3, fill=color)

        pdf = io.BytesIO()
        img.save(pdf,"PDF")

        z.writestr(f"{str(i+1).zfill(3)}_{t1}.pdf", pdf.getvalue())
        prog.progress((i+1)/len(df))

    z.close()
    generate_area.download_button("📦 Download ZIP", zip_buffer.getvalue(), "sertifikat_3field.zip")