import fitz  # PyMuPDF
import os
from io import BytesIO

working_dir = os.path.expanduser("~")


def compress_pdf_fitz(
    input_path,
    output_path,
    target_size_kb=200,
    initial_dpi=120,
    min_dpi=60,
    initial_jpg_quality=70,
    min_jpg_quality=30,
    dpi_step=0.85,
    quality_step=5,
):
    """
    Compress a PDF toward target_size_kb using PyMuPDF.
    Converts each page to JPEG and rebuilds a lightweight PDF.
    (Resulting PDF will be image-only.)
    """

    # Open source file
    src = fitz.open(input_path)

    dpi = initial_dpi
    jpg_quality = initial_jpg_quality

    while True:
        out = fitz.open()
        zoom = dpi / 72.0  # scaling factor

        # Convert each page to image and reinsert
        for page in src:
            rect = page.rect
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            img_bytes = pix.tobytes(output="jpg", jpg_quality=jpg_quality)

            new_page = out.new_page(width=rect.width, height=rect.height)
            new_page.insert_image(new_page.rect, stream=img_bytes)

        # Save temporary result to memory
        buffer = BytesIO()
        out.save(buffer, garbage=4, deflate=True, clean=True)
        out.close()

        size_kb = len(buffer.getvalue()) / 1024
        print(f"→ {dpi:.0f} DPI | JPEG {jpg_quality}% | Size: {size_kb:.1f} KB")

        # Check if we met target
        if size_kb <= target_size_kb or (dpi <= min_dpi and jpg_quality <= min_jpg_quality):
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            print(f"\n✅ Final saved: {output_path} ({size_kb:.1f} KB)")
            break

        # Otherwise, reduce quality first, then DPI
        if jpg_quality > min_jpg_quality:
            jpg_quality = max(min_jpg_quality, jpg_quality - quality_step)
        else:
            dpi = int(max(min_dpi, dpi * dpi_step))

    src.close()

def start_compress_pdf():
    # Example usage:
    # def start_compress_pdf():
    input_path = working_dir
    pdf_filename = input("Enter pdf file name:- ")
    output_path = input_path + '\\compressed_pdf'
    os.makedirs(output_path, exist_ok=True)

    target_size = int(input("Enter target size in kbs:- "))


    # for pdf_file in os.listdir(input_path):
    #     # print(pdf_file,pdf_file[-4:])
    #     if pdf_file != 'compress_pdf.bat' and pdf_file[-4:] == '.pdf':
    #         file_name = os.path.splitext(os.path.basename(pdf_file))[0]

    input_file_name = input_path + "\\" + pdf_filename
    output_file_name = output_path + "\\" + pdf_filename

    print(input_file_name, output_file_name)

    compress_pdf_fitz(
        input_path=input_file_name,
        output_path=output_file_name,
        target_size_kb=target_size,
        initial_dpi=200,
        min_dpi=50,
        initial_jpg_quality=95,
        min_jpg_quality=20,
    )

if __name__ == "__main__":
    start_compress_pdf()