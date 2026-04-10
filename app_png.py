from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

# Config
template_path = "template/template1.png"
output_folder = "output"
font_path = "arial.ttf"
font_size = 60

# Posisi Y manual (atur sesuai desain sertifikat)
text_y = 600  

# Setup
os.makedirs(output_folder, exist_ok=True)
data = pd.read_csv("daftar_nama.csv")
font = ImageFont.truetype(font_path, font_size)

for index, row in data.iterrows():
    nama = row['nama']

    # Load template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Ambil ukuran gambar
    image_width, image_height = image.size

    # Hitung ukuran teks
    bbox = draw.textbbox((0, 0), nama, font=font)
    text_width = bbox[2] - bbox[0]

    # Hitung posisi X agar center
    text_x = (image_width - text_width) / 2

    # Gambar teks
    draw.text((text_x, text_y), nama, font=font, fill="black")

    # Simpan
    filename = nama.replace(" ", "_")
    output_path = f"{output_folder}/sertifikat_{filename}.png"
    image.save(output_path)

    print(f"Generated: {output_path}")

print("Semua sertifikat berhasil dibuat!")