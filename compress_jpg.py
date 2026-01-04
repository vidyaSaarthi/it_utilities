from pdf2image import convert_from_path
from PIL import Image
import os

def compress_image(input_path, output_path, target_kb):
    img = Image.open(input_path)
    quality = 95  # Start high, reduce until target met

    while True:
        print(output_path)
        img.save(output_path, "JPEG", quality=quality)
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_kb or quality <= 5:
            break
        quality -= 5

    print(f"Compressed {input_path} → {size_kb:.1f} KB")


path = input("Enter path of the Jpg file:- ")
jpg_filename = input("Enter jpg file name:- ")
target_size_kb = int(input("Enter target size in kbs:- "))

# path=r"C:\Users\Shubham Aggarwal\Downloads"
# jpg_filename = r"\Wisdom Reasoning Olympiad  OMR Sheet (1)_page_3.jpg"
# target_size_kb = 290

compressed_folder = path + r"\compressed_images"
os.makedirs(compressed_folder, exist_ok=True)



compress_image(path + '\\' + jpg_filename , compressed_folder + jpg_filename, target_size_kb)