import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io, os, uuid
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
    </style>""", unsafe_allow_html=True)


render_sidebar()

st.markdown("<h1 style='text-align:center;'>Generator Single Input</h1>", unsafe_allow_html=True)

# ================= INIT =================
if "fields" not in st.session_state:
    st.session_state.fields = [{"id": str(uuid.uuid4())}]  # minimal 1 field

# ================= FONT =================
fonts = {}
if os.path.exists("fonts"):
    for f in os.listdir("fonts"):
        if f.endswith(".ttf"):
            fonts[f.replace(".ttf","")] = os.path.join("fonts", f)

# ================= FUNCTION =================
def pos(label, default_y, field_id, index):
    colA, colB = st.columns([6,1])

    with colA:
        with st.expander(label, expanded=(index == 0)):
            text = st.text_input(f"{label}", "", key=f"text_{field_id}")
            size = st.slider(f"Font {label}", 20,150,60, key=f"size_{field_id}")
            mode = st.selectbox(label, ["Center","Left","Right","Custom"], key=f"mode_{field_id}")
            x = st.number_input(f"X {label}", value=100, key=f"x_{field_id}") if mode=="Custom" else None
            y = st.number_input(f"Y {label}", value=default_y, key=f"y_{field_id}")

    delete_clicked = False
    if index != 0:
        with colB:
            if st.button("❌", key=f"delete_{field_id}"):
                delete_clicked = True

    return {
        "id": field_id,
        "text": text,
        "mode": mode,
        "x": x,
        "y": y,
        "size": size,
        "delete": delete_clicked
    }

def get_x(mode, x, w_img, w_text):
    if mode=="Center": return (w_img-w_text)/2
    if mode=="Left": return 50
    if mode=="Right": return w_img-w_text-50
    return x

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

with col1:
    template_file = st.file_uploader("Template", type=["jpg", "jpeg", "png"])
    font_name = st.selectbox("Font", list(fonts.keys())) if fonts else None
    color = st.color_picker("Warna Font", "#000000")

    # ➕ tambah field
    if st.button("➕ Tambah Input"):
        st.session_state.fields.append({"id": str(uuid.uuid4())})

    st.markdown("### ⚙️ Pengaturan Input")

    new_fields = []
    delete_id = None

    for i, f in enumerate(st.session_state.fields):
        label = f"Input {i+1}"

        field = pos(label, 600 + (i * 80), f["id"], i)

        if field["delete"]:
            delete_id = f["id"]
        else:
            new_fields.append(field)

    # 🔥 hapus berdasarkan ID (FIX)
    if delete_id:
        st.session_state.fields = [
            f for f in st.session_state.fields if f["id"] != delete_id
        ]
        st.rerun()

    preview = st.button("👁️ Preview")
    generate = st.button("📄 Generate PDF")


with col2:
    preview_area = st.container()
    generate_area = st.container()

# ================= PREVIEW =================
if preview and template_file and font_name:
    img = Image.open(template_file).convert("RGB")
    d = ImageDraw.Draw(img)
    w,_ = img.size

    for f in new_fields:
        font = ImageFont.truetype(fonts[font_name], f["size"])
        text_width = d.textbbox((0,0), f["text"], font=font)[2]

        d.text(
            (get_x(f["mode"], f["x"], w, text_width), f["y"]),
            f["text"],
            font=font,
            fill=color
        )

    preview_area.image(img)

# ================= GENERATE =================
if generate and template_file and font_name:
    img = Image.open(template_file).convert("RGB")
    d = ImageDraw.Draw(img)
    w,_ = img.size

    for f in new_fields:
        font = ImageFont.truetype(fonts[font_name], f["size"])
        text_width = d.textbbox((0,0), f["text"], font=font)[2]

        d.text(
            (get_x(f["mode"], f["x"], w, text_width), f["y"]),
            f["text"],
            font=font,
            fill=color
        )

    pdf = io.BytesIO()
    img.save(pdf, "PDF")

    filename = new_fields[0]["text"] if new_fields else "output"

    generate_area.download_button(
        "📄 Download PDF",
        pdf.getvalue(),
        f"{filename}.pdf"
    )