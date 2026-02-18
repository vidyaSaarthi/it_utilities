import fitz  # PyMuPDF
import os.path  # Python's standard path module
import glob
import os

working_dir = os.path.expanduser("~")
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

def start_pdf_to_jpg():
    # Replace 'input.pdf' with the actual path to your PDF file.
    # Make sure the PDF file exists in the same directory, or provide a full path.
    user_input = input("Enter your options:-\n1 - Single Pdf\n2 - All pdfs In A Directory\n")

    if int(user_input) == 1:
        pdf_path = working_dir
        pdf_name = input("Enter pdf File Name:- ")

        input_pdf_file = pdf_path + '\\' + pdf_name
        output_jpg_path = working_dir + "\\pdf_to_jpg"
        os.makedirs(output_jpg_path, exist_ok=True)

        pdf_to_jpg_corrected(input_pdf_file, output_dir = output_jpg_path)

    elif int(user_input) == 2:
        pdf_path = working_dir
        pdf_files = glob.glob(os.path.join(pdf_path, "*.pdf"))
        output_jpg_path = working_dir + "\\pdf_to_jpg"

        for each_pdf_file in pdf_files:
            pdf_to_jpg_corrected(each_pdf_file, output_dir=output_jpg_path)

if __name__ == "__main__":
    start_pdf_to_jpg()