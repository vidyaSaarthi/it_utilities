import win32com.client
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io, os

location=r"H:\My Drive\Business\Vidya Saarthi\Counselling\MBBS\2025 Counselling Artifacts\States 2025 notices\MCC\\"
# Paths
file_name='Deemed Colleges Cut Off Round 1'
input_excel=location + file_name + '.xlsx'
output_pdf_file=location + file_name + '_temp.pdf'

# Start Excel
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

# Open Workbook
wb = excel.Workbooks.Open(input_excel)
ws = wb.Sheets("BDS")

# Page setup: landscape, fit to page
ws.PageSetup.Orientation = 2  # 2 = xlLandscape
ws.PageSetup.Zoom = False
ws.PageSetup.FitToPagesWide = 1
ws.PageSetup.FitToPagesTall = False  # fit width only, don't shrink height

# Export as PDF
wb.ExportAsFixedFormat(0, output_pdf_file)

# Cleanup
wb.Close(False)
excel.Quit()


# Load your logo image
logo_path = r"H:\My Drive\Business\Vidya Saarthi\Logo\VidyaSaarthi.jpg"  # Make sure path is correct
existing_pdf_file = output_pdf_file


# Paths
# logo_path = "vidyasaarthi_logo.png"
# source_pdf_path = "output.pdf"
# output_pdf_path = "output_with_logo_watermark.pdf"

# Step 1: Read the first page of PDF to get actual dimensions
pdf_reader = PdfReader(existing_pdf_file)
first_page = pdf_reader.pages[0]
media_box = first_page.mediabox

page_width = float(media_box.width)
page_height = float(media_box.height)

# Step 2: Create watermark PDF in memory with same size
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=(page_width, page_height))

# Add logo covering the full page
logo = ImageReader(logo_path)
c.setFillAlpha(0.15)
c.drawImage(logo, 0, 0, width=page_width, height=page_height, mask='auto')
c.save()
packet.seek(0)

# Step 3: Apply watermark to each page
watermark_reader = PdfReader(packet)
watermark_page = watermark_reader.pages[0]
output_pdf = PdfWriter()

for page in pdf_reader.pages:
    page.merge_page(watermark_page)
    output_pdf.add_page(page)

# Step 4: Save final watermarked PDF
output_final_pdf_file=location + file_name + '.pdf'

with open(output_final_pdf_file, "wb") as f:
    output_pdf.write(f)

os.remove(output_pdf_file)
