# from PIL import Image
# import os
# # from pdf_to_jpg import working_dir
# working_dir = r"H:\My Drive\Business\Vidya Saarthi\IT\utilities"
#
# def convert_jpg_to_pdf(jpg_path, pdf_path):
#     """
#     Converts a single JPG image file to a PDF file.
#
#     Args:
#         jpg_path (str): The full path to the input JPG file.
#         pdf_path (str): The full path for the output PDF file.
#     """
#     print(jpg_path,pdf_path)
#     try:
#         # 1. Open the image using the Pillow library
#         image = Image.open(jpg_path)
#
#         # 2. Convert the image to RGB if it's in a different mode (like L for grayscale
#         #    or RGBA which can cause issues with PDF saving)
#         if image.mode == 'RGBA':
#             image = image.convert('RGB')
#
#         # 3. Save the image as a PDF file
#         # The 'save' method handles the conversion based on the file extension (.pdf)
#         image.save(pdf_path, 'PDF')
#
#         print(f"✅ Successfully converted '{os.path.basename(jpg_path)}' to '{os.path.basename(pdf_path)}'.")
#
#     except FileNotFoundError:
#         print(f"❌ Error: The file '{jpg_path}' was not found.")
#     except Exception as e:
#         print(f"❌ An error occurred during conversion: {e}")
#
#
# def start_jpg_to_pdf():
#     jpg_path = working_dir
#     INPUT_JPG_FILE = input("Enter JPG/JPEG File Name:- ")
#     INPUT_JPG_FILE_FINAL= jpg_path + "\\" + INPUT_JPG_FILE
#
#     # 2. Define the output PDF file path
#     OUTPUT_PDF_FILE_PATH = jpg_path + "\\jpg_to_pdf"
#     os.makedirs(OUTPUT_PDF_FILE_PATH, exist_ok=True)
#
#     # Run the conversion
#     convert_jpg_to_pdf(INPUT_JPG_FILE_FINAL, OUTPUT_PDF_FILE_PATH + "\\" + INPUT_JPG_FILE.split(".")[0] + ".pdf")
#
# start_jpg_to_pdf()

from PIL import Image
import os

# Updated working directory
working_dir = r"H:\My Drive\Business\Vidya Saarthi\IT\utilities"


def convert_multiple_jpgs_to_pdf(jpg_paths, output_pdf_path):
    """
    Converts multiple JPG images into a single multi-page PDF.
    """
    images = []

    try:
        for path in jpg_paths:
            img = Image.open(path)
            # Ensure all images are in RGB mode for PDF compatibility
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)

        if images:
            # Save the first image and append the rest
            images[0].save(
                output_pdf_path,
                save_all=True,
                append_images=images[1:],
                resolution=100.0,
                quality=95
            )
            print(f"✅ Successfully created: {os.path.basename(output_pdf_path)}")
        else:
            print("❌ No valid images found to convert.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")


def start_jpg_to_pdf_multi():
    # 1. Setup paths
    output_folder = os.path.join(working_dir, "jpg_to_pdf")
    os.makedirs(output_folder, exist_ok=True)

    # 2. Get input from user (comma separated for multiple files)
    print("Enter JPG/JPEG File Names (e.g., image1.jpg, image2.jpg):")
    input_str = input(">> ")

    # Clean up file names and create full paths
    file_names = [f.strip() for f in input_str.split(",")]
    full_paths = [os.path.join(working_dir, name) for name in file_names]

    # 3. Define output name (uses the first filename as a base)
    if file_names:
        output_filename = file_names[0].split(".")[0] + "_merged.pdf"
        final_pdf_path = os.path.join(output_folder, output_filename)

        # Run the conversion
        convert_multiple_jpgs_to_pdf(full_paths, final_pdf_path)


if __name__ == "__main__":
    start_jpg_to_pdf_multi()