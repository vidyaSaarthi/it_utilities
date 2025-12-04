from pdf2image import convert_from_path
from PIL import Image
import os

def compress_image(input_path, output_path, target_kb):
    img = Image.open(input_path)
    quality = 95  # Start high, reduce until target met

    while True:
        img.save(output_path, "JPEG", quality=quality)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb or quality <= 5:
            break
        quality -= 5

    print(f"Compressed {input_path} → {size_kb:.1f} KB")


target_size_kb = 490

path=r'H:\My Drive\Business\Vidya Saarthi\Forms Automation\Haryana NEET UG Form\Suhani'
compressed_folder = "\compressed_images"
os.makedirs(path + compressed_folder, exist_ok=True)
file='Photo.jpeg'

compressed_path = os.path.join(compressed_folder, os.path.basename(jpg))
compress_image(jpg, compressed_path, target_size_kb)