import time
from PIL import Image
import os

working_dir = os.path.expanduser("~")
def compress_image(input_path, output_path, target_kb):
    img = Image.open(input_path)
    quality = 95  # Start high, reduce until target met
    print(f"{input_path} to {output_path} with target size as {target_kb}\n\n")

    # aspect_ratio = img.height / img.width
    # new_width = 1000
    # new_height = int(new_width * aspect_ratio)
    # img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    resize_factor = 0.9  # Reduce dimensions by 10% if needed

    while True:
        print(f"Compressing {input_path} to {output_path} with {quality}")
        img.save(output_path, "JPEG", quality=quality)
        time.sleep(2)
        size_kb = os.path.getsize(output_path) / 1024
        print(size_kb)
        if size_kb <= target_kb:
            print(f"✅ Success! Image compressed to size_kb KB")
            break

        if quality > 20:
            print("Reducing Quality by -5")
            quality -= 5
        else:
            # If quality is already trash (20), start resizing the image dimensions
            new_width = int(img.width * resize_factor)
            new_height = int(img.height * resize_factor)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Reset quality slightly to avoid getting stuck at low quality + small size
            quality = 60

            print("Reducing Resize factor")
            resize_factor = resize_factor - 0.1

    print(f"Compressed {input_path} → {size_kb:.1f} KB at {output_path}")

def start_compress_jpg():

    path = working_dir
    jpg_filename = input("Enter jpg file name:- ")
    target_size_kb = int(input("Enter target size in kbs:- "))

    compressed_folder = path + r"\\compressed_jpg\\"
    os.makedirs(compressed_folder, exist_ok=True)

    compress_image(path + '\\' + jpg_filename , compressed_folder + jpg_filename, target_size_kb)

if __name__ == "__main__":
    start_compress_jpg()