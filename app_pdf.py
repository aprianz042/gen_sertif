from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

template_path = "template/template2.jpeg"
output_folder = "output_pdf"
font_path = "fonts/Segoe UI Bold.ttf"
font_size = 60
text_y = 430

os.makedirs(output_folder, exist_ok=True)
data = pd.read_csv("data_n.csv")
font = ImageFont.truetype(font_path, font_size)

for index, row in data.iterrows():
    nama = row['nama']

    image = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    image_width, _ = image.size

    bbox = draw.textbbox((0, 0), nama, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (image_width - text_width) / 2

    draw.text((text_x, text_y), nama, font=font, fill="black")

    filename = nama.replace(" ", "_")
    output_path = f"{output_folder}/{filename}.pdf"

    image.save(output_path, "PDF", resolution=100.0)

    print(f"Generated: {output_path}")

print("Selesai!")