from PIL import Image
import os


def convert_jpg_to_pdf(jpg_path, pdf_path):
    """
    Converts a single JPG image file to a PDF file.

    Args:
        jpg_path (str): The full path to the input JPG file.
        pdf_path (str): The full path for the output PDF file.
    """
    try:
        # 1. Open the image using the Pillow library
        image = Image.open(jpg_path)

        # 2. Convert the image to RGB if it's in a different mode (like L for grayscale 
        #    or RGBA which can cause issues with PDF saving)
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # 3. Save the image as a PDF file
        # The 'save' method handles the conversion based on the file extension (.pdf)
        image.save(pdf_path, 'PDF')

        print(f"✅ Successfully converted '{os.path.basename(jpg_path)}' to '{os.path.basename(pdf_path)}'.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{jpg_path}' was not found.")
    except Exception as e:
        print(f"❌ An error occurred during conversion: {e}")


# --- Example Usage ---

# 1. Define the input JPG file path
#    (Make sure you have an image named 'input_image.jpg' in the same directory, 
#    or provide the full path)
INPUT_JPG_FILE = r"C:\Users\Shubham Aggarwal\Downloads\WhatsApp Image 2025-12-25 at 12.31.50 PM.jpeg"

# 2. Define the output PDF file path
OUTPUT_PDF_FILE = r"C:\Users\Shubham Aggarwal\Downloads\WhatsApp Image 2025-12-25 at 12.31.50 PM.pdf"

# Run the conversion
convert_jpg_to_pdf(INPUT_JPG_FILE, OUTPUT_PDF_FILE)