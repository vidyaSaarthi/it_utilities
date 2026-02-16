from PIL import Image
import os
# from pdf_to_jpg import working_dir
working_dir = r"H:\My Drive\Business\Vidya Saarthi\IT\utilities"

def convert_jpg_to_pdf(jpg_path, pdf_path):
    """
    Converts a single JPG image file to a PDF file.

    Args:
        jpg_path (str): The full path to the input JPG file.
        pdf_path (str): The full path for the output PDF file.
    """
    print(jpg_path,pdf_path)
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


def start_jpg_to_pdf():
    jpg_path = working_dir
    INPUT_JPG_FILE = input("Enter JPG/JPEG File Name:- ")
    INPUT_JPG_FILE_FINAL= jpg_path + "\\" + INPUT_JPG_FILE

    # 2. Define the output PDF file path
    OUTPUT_PDF_FILE_PATH = jpg_path + "\\jpg_to_pdf"
    os.makedirs(OUTPUT_PDF_FILE_PATH, exist_ok=True)

    # Run the conversion
    convert_jpg_to_pdf(INPUT_JPG_FILE_FINAL, OUTPUT_PDF_FILE_PATH + "\\" + INPUT_JPG_FILE.split(".")[0] + ".pdf")

start_jpg_to_pdf()