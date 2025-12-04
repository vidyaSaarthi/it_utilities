# import fitz  # PyMuPDF
# from PIL import Image
# import os
#
# # 📂 Input folder containing PDFs
# input_folder = r'H:\My Drive\Business\Vidya Saarthi\Counselling\MBBS\2025 Counselling Artifacts\Customer Documents\Shaurya Aggarwal'
# # 📂 Output folder for converted images
# output_folder = input_folder + r'\out'
# # 📂 Output folder for compressed images
# compressed_folder = input_folder + r'\compressed'
#
# os.makedirs(output_folder, exist_ok=True)
# os.makedirs(compressed_folder, exist_ok=True)
#
# def compress_image_to_size(input_img, output_path, target_kb=500):
#     """Compress and resize image until it's under target_kb size."""
#     img = input_img.copy()
#     quality = 95
#
#     while True:
#         img.save(output_path, "JPEG", quality=quality)
#         size_kb = os.path.getsize(output_path) / 1024
#
#         if size_kb <= target_kb:
#             break
#
#         if quality > 10:
#             quality -= 5
#         else:
#             # Resize image by 80% if quality can't go lower
#             w, h = img.size
#             img = img.resize((int(w * 0.6), int(h * 0.6)), Image.LANCZOS)
#
#     print(f"✅ {os.path.basename(output_path)} → {size_kb:.1f} KB")
#
# # Loop over all PDFs in the folder
# for filename in os.listdir(input_folder):
#     if filename.lower().endswith(".pdf"):
#         pdf_path = os.path.join(input_folder, filename)
#         base_name = os.path.splitext(filename)[0]
#         print(f"📄 Processing: {pdf_path}")
#
#         pdf_doc = fitz.open(pdf_path)
#
#         for page_number in range(len(pdf_doc)):
#             page = pdf_doc[page_number]
#             pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher matrix = better quality
#             img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#
#             jpg_filename = f"{base_name}_page_{page_number+1}.jpg"
#             jpg_path = os.path.join(output_folder, jpg_filename)
#             pix.save(jpg_path)
#
#             # Compress the JPG
#             compressed_path = os.path.join(compressed_folder, jpg_filename)
#             compress_image_to_size(img, compressed_path, target_kb=500)
#
#         pdf_doc.close()
#
# print("✅ All PDFs processed successfully!")


import fitz  # PyMuPDF
import os.path  # Python's standard path module
import glob
import os


def pdf_to_jpg_corrected(pdf_path, output_dir=".", zoom_x=2.0, zoom_y=2.0, rotation=0):
    """
    Converts each page of a PDF file to a separate JPG image using os.path
    for robust path handling, replacing fitz.path_split/path_join.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: The file was not found at {pdf_path}")
        return

    try:
        # 1. Open the PDF document
        document = fitz.open(pdf_path)
        print(f"Opened PDF: {pdf_path}")

        # 2. Setup transformation matrix for high resolution
        matrix = fitz.Matrix(zoom_x, zoom_y, rotation)

        # Extract the base name (without extension) for the output files
        # os.path.basename returns 'input.pdf'
        # os.path.splitext splits it into ('input', '.pdf')
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # 3. Iterate through all pages
        for page_num in range(len(document)):
            page = document.load_page(page_num)  # Load the current page

            # Render the page to a pixmap
            pix = page.get_pixmap(matrix=matrix, alpha=False)

            # Create the output filename: e.g., 'document_page_1.jpg'
            output_filename = f"{base_name}_page_{page_num + 1}.jpg"

            # Join the directory and filename using os.path.join
            output_path = os.path.join(output_dir, output_filename)

            # Save the pixmap to a JPG file
            pix.save(output_path)
            print(f"Successfully saved: {output_path}")

        document.close()
        print("\nConversion complete.")

    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}")


# Replace 'input.pdf' with the actual path to your PDF file.
# Make sure the PDF file exists in the same directory, or provide a full path.
user_input = input("Enter your options:-\n1 - Single Pdf\n2 - All pdfs In A Directory\n")

if int(user_input) == 1:
    pdf_path = input("Enter pdf Path:- ")
    pdf_name = input("Enter pdf File Name:- ")

    input_pdf_file = pdf_path + '\\' + pdf_name
    output_jpg_path = pdf_path

    pdf_to_jpg_corrected(input_pdf_file, output_dir = output_jpg_path)

elif int(user_input) == 2:
    pdf_path = input("Enter pdfs Path:- ")
    pdf_files = glob.glob(os.path.join(pdf_path, "*.pdf"))

    for each_pdf_file in pdf_files:
        pdf_to_jpg_corrected(each_pdf_file, output_dir=pdf_path)
