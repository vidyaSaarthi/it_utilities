from rembg import remove
from PIL import Image

# Input and output file paths
input_path = r"C:\Users\Shubham Aggarwal\Downloads\RR_test.jpeg"
output_path = r"C:\Users\Shubham Aggarwal\Downloads\RR_test.png"

# Open the image
input_image = Image.open(input_path)

# Remove the background
output_image = remove(input_image)

# Save result as PNG (to keep transparency)
# output_image.save(output_path)

# print(f"✅ Background removed successfully! Saved as: {output_path}")

# Convert to RGBA first
output_image = output_image.convert("RGBA")

# Create white background
white_bg = Image.new("RGBA", output_image.size, "WHITE")
white_bg.paste(output_image, (0, 0), output_image)
white_bg.convert("RGB").save(output_path, "JPEG")

