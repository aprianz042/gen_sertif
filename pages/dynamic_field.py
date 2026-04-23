import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io, os, zipfile
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

st.markdown("<h1 style='text-align:center;'>Generator Dynamic Field</h1>", unsafe_allow_html=True)

# ================= FONT =================
fonts = {}
if os.path.exists("fonts"):
    for f in os.listdir("fonts"):
        if f.endswith(".ttf"):
            fonts[f.replace(".ttf","")] = os.path.join("fonts", f)

# ================= FUNCTION =================
def pos(label, default_y, expanded=False):
    with st.expander(label, expanded):
        size = st.slider(f"Font {label}", 20,150,60, key=label+"_size")
        mode = st.selectbox(label, ["Center","Left","Right","Custom"], key=label+"_mode")
        x = st.number_input(f"X {label}", value=100, key=label+"_x") if mode=="Custom" else None
        y = st.number_input(f"Y {label}", value=default_y, key=label+"_y")
    return mode, x, y, size

def get_x(mode, x, w_img, w_text):
    if mode=="Center": return (w_img-w_text)/2
    if mode=="Left": return 50
    if mode=="Right": return w_img-w_text-50
    return x

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

with col1:
    template_file = st.file_uploader("Template", type=["jpg", "jpeg", "png"])
    csv_file = st.file_uploader("CSV", type=["csv"])

    font_name = st.selectbox("Font", list(fonts.keys())) if fonts else None
    color = st.color_picker("Warna Font", "#000000")

    fields = []
    df = None

    # ================= READ CSV =================
    if csv_file:
        try:
            csv_file.seek(0)
            df = pd.read_csv(csv_file, dtype=str)

            if df.empty:
                st.warning("CSV kosong")
                st.stop()

            headers = list(df.columns)

            st.markdown("### ⚙️ Pengaturan Field")

            for i, col in enumerate(headers):
                label = col.replace("_", " ").title()

                mode, x, y, size = pos(
                    label,
                    600 + (i * 80),
                    expanded=(i == 0)
                )

                fields.append({
                    "col": col,
                    "mode": mode,
                    "x": x,
                    "y": y,
                    "size": size
                })

        except Exception as e:
            st.error(f"CSV error: {e}")
            st.stop()

    preview = st.button("👁️ Preview")
    generate = st.button("🚀 Generate")

with col2:
    preview_area = st.container()
    generate_area = st.container()

# ================= PREVIEW =================
if preview and csv_file and template_file and font_name:
    csv_file.seek(0)
    df = pd.read_csv(csv_file, dtype=str)
    r = df.iloc[0]

    img = Image.open(template_file).convert("RGB")
    d = ImageDraw.Draw(img)
    w,_ = img.size

    for f in fields:
        value = str(r[f["col"]])

        font = ImageFont.truetype(fonts[font_name], f["size"])
        text_width = d.textbbox((0,0), value, font=font)[2]

        d.text(
            (get_x(f["mode"], f["x"], w, text_width), f["y"]),
            value,
            font=font,
            fill=color
        )

    preview_area.image(img, caption="Preview")

# ================= GENERATE =================
if generate and csv_file and template_file and font_name:
    csv_file.seek(0)
    df = pd.read_csv(csv_file, dtype=str)

    zip_buffer = io.BytesIO()
    z = zipfile.ZipFile(zip_buffer,"w")

    prog = generate_area.progress(0)

    for i,row in df.iterrows():
        img = Image.open(template_file).convert("RGB")
        d = ImageDraw.Draw(img)
        w,_ = img.size

        for f in fields:
            value = str(row[f["col"]])

            font = ImageFont.truetype(fonts[font_name], f["size"])
            text_width = d.textbbox((0,0), value, font=font)[2]

            d.text(
                (get_x(f["mode"], f["x"], w, text_width), f["y"]),
                value,
                font=font,
                fill=color
            )

        pdf = io.BytesIO()
        img.save(pdf,"PDF")

        # nama file dari kolom pertama
        filename = str(row[fields[0]["col"]]).replace(" ", "_")

        z.writestr(f"{str(i+1).zfill(3)}_{filename}.pdf", pdf.getvalue())
        prog.progress((i+1)/len(df))

    z.close()

    generate_area.download_button(
        "📦 Download ZIP",
        zip_buffer.getvalue(),
        "sertifikat_auto.zip"
    )