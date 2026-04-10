from PIL import Image, ImageDraw, ImageFont
import os

# =========================
# CONFIG
# =========================
template_path = "template/template2.jpeg"
output_folder = "preview"
font_path = "fonts/Segoe UI Bold.ttf"
font_size = 60
text_y = 430

# Nama dummy
nama = "Budi Santoso"

# =========================
# SETUP
# =========================
os.makedirs(output_folder, exist_ok=True)

font = ImageFont.truetype(font_path, font_size)

# =========================
# PROCESS
# =========================
image = Image.open(template_path).convert("RGB")
draw = ImageDraw.Draw(image)

image_width, _ = image.size

# Hitung center horizontal
bbox = draw.textbbox((0, 0), nama, font=font)
text_width = bbox[2] - bbox[0]
text_x = (image_width - text_width) / 2

# Gambar teks
draw.text((text_x, text_y), nama, font=font, fill="black")

# =========================
# OUTPUT
# =========================
output_path = f"{output_folder}/test_dummy.pdf"
image.save(output_path, "PDF", resolution=100.0)

print(f"Generated: {output_path}")
print("Selesai (mode dummy 1 nama)!")