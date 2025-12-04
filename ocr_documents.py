"""
Extract roll number and subject marks from a CBSE marksheet image.

Input image path: adjust image_path variable if required.
"""

import re
import cv2
import pytesseract
from PIL import Image
import numpy as np
import pandas as pd

# Path to your image (change if needed)
image_path = "/mnt/data/10th DMC.jpeg"

# Optional: If Tesseract isn't in PATH, set pytesseract.pytesseract.tesseract_cmd
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_for_ocr(img_bgr):
    """Convert to gray, denoise, and adaptive threshold to improve OCR."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # Resize (helps OCR on small text)
    scale = 1.5
    h, w = gray.shape
    gray = cv2.resize(gray, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_LINEAR)
    # Apply bilateral filter to preserve edges
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    # Adaptive threshold
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 15, 8)
    return th

def ocr_image_to_text(img_bgr):
    """Return OCR text for BGR image (OpenCV) after preprocessing."""
    pre = preprocess_for_ocr(img_bgr)
    pil = Image.fromarray(pre)
    txt = pytesseract.image_to_string(pil, lang='eng')
    return txt

def find_roll_number(text):
    """Try several regex patterns to find roll number (6-12 digits typical)."""
    patterns = [
        r'Roll\s*No[:\.\s-]*([0-9]{5,12})',
        r'Roll\s*No\.?[:\s]*([0-9]{5,12})',
        r'Roll\s*Number[:\s]*([0-9]{5,12})',
        r'\b([0-9]{7,9})\b'  # fallback: any 7-9 digit number (may false-positive)
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            return m.group(1)
    return None

def crop_region(img_bgr, x_frac=(0.05,0.55), y_frac=(0.05,0.28)):
    """Crop a region using fractional coordinates of width/height."""
    h, w = img_bgr.shape[:2]
    x1 = int(w * x_frac[0]); x2 = int(w * x_frac[1])
    y1 = int(h * y_frac[0]); y2 = int(h * y_frac[1])
    return img_bgr[y1:y2, x1:x2]

def extract_table_text_blocks(img_bgr):
    """
    Use pytesseract image_to_data to get lines with their bounding boxes.
    Returns a list of tuples: (line_text, left, top, width, height).
    """
    pre = preprocess_for_ocr(img_bgr)
    # Use OEM/LSTM default; get TSV data
    data = pytesseract.image_to_data(pre, lang='eng', output_type=pytesseract.Output.DATAFRAME)
    data = data.dropna(subset=['text'])
    # group by line_num (and block_num) to get line-wise text
    rows = []
    if not data.empty:
        grouped = data.groupby(['block_num','par_num','line_num'])
        for _, g in grouped:
            line_text = " ".join(g['text'].astype(str).tolist()).strip()
            left = int(g['left'].min())
            top = int(g['top'].min())
            width = int(g['left'].max() + g['width'].max() - left)
            height = int(g['top'].max() + g['height'].max() - top)
            rows.append((line_text, left, top, width, height))
    return rows

def parse_subject_rows_from_lines(lines_text):
    """
    Parse subject rows using regex.
    Expected formats (examples from your image):
    '085   HINDI COURSE-B   046 017 063   SIXTY THREE   D1'
    '041 MATHEMATICS STANDARD 028 016 044 FORTY FOUR D1'
    Also an additional subject row like '402 INFORMATION TECHNOLOGY 022 050 072 SEVENTY TWO C1'
    """
    subjects = []
    # regex to capture: subject code (3 digits), subject name (letters, &, ., - and spaces),
    # theory (2-3 digits), internal (2-3 digits), total (2-3 digits)
    subj_pattern = re.compile(r'\b(\d{3})\b\s+([A-Z&\-\.\s0-9]{4,80}?)\s+(\d{2,3})\s+(\d{2,3})\s+(\d{2,3})\b', flags=re.IGNORECASE)
    for line in lines_text:
        t = line[0]
        m = subj_pattern.search(t)
        if m:
            code = m.group(1).strip()
            name = m.group(2).strip()
            th = m.group(3).strip()
            internal = m.group(4).strip()
            total = m.group(5).strip()
            # cleanup name: remove stray numbers and repeated spaces
            name = re.sub(r'\s{2,}', ' ', name)
            # Trim trailing digits that sometimes remain in name
            name = re.sub(r'\s+\d+$', '', name).strip()
            subjects.append({
                'Subject Code': code,
                'Subject': name.title(),
                'Theory Marks': th,
                'Internal Marks': internal,
                'Total Marks': total
            })
    return subjects

def main(image_path):
    # Read image with OpenCV
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    # 1) Whole-image OCR to try to find roll number
    full_text = ocr_image_to_text(img_bgr)
    roll = find_roll_number(full_text)
    print("Roll found from full image OCR:", roll)

    # 2) If not found, crop the top-left region (where roll number usually sits) and retry
    if not roll:
        crop = crop_region(img_bgr, x_frac=(0.02, 0.55), y_frac=(0.08, 0.28))
        crop_text = ocr_image_to_text(crop)
        roll = find_roll_number(crop_text)
        print("Roll found from top-left crop OCR:", roll)

    # 3) If still not found try more aggressive crop near the cert area
    if not roll:
        crop2 = crop_region(img_bgr, x_frac=(0.02, 0.45), y_frac=(0.05, 0.18))
        crop2_text = ocr_image_to_text(crop2)
        roll = find_roll_number(crop2_text)
        print("Roll found from smaller crop OCR:", roll)

    # 4) Extract table lines (lines from the OCR data)
    lines = extract_table_text_blocks(img_bgr)
    # lines is a list of (text, left, top, width, height). We sort by top coordinate to keep table order.
    lines_sorted = sorted(lines, key=lambda x: x[2])
    # Print sample of lines found for debugging (optional)
    # for l in lines_sorted[:30]:
    #     print(l[0])

    # 5) Parse subject rows
    subjects = parse_subject_rows_from_lines(lines_sorted)

    # If we found nothing via the general parser, attempt to search only lower half (table region)
    if not subjects:
        h = img_bgr.shape[0]
        table_crop = img_bgr[int(h*0.28):int(h*0.85), :]
        lines2 = extract_table_text_blocks(table_crop)
        lines2_sorted = sorted(lines2, key=lambda x: x[2])
        subjects = parse_subject_rows_from_lines(lines2_sorted)

    # Convert to DataFrame for pretty output
    df = pd.DataFrame(subjects)

    print("\nExtracted Subjects DataFrame:")
    if df.empty:
        print("No subject rows parsed automatically. You may need to tweak cropping or regex.")
    else:
        print(df.to_string(index=False))

    print("\nFull OCR text (first 800 chars for reference):\n")
    print(full_text[:800])

    return roll, df, full_text

if __name__ == "__main__":
    roll_number, subjects_df, ocr_text = main(image_path)
    print("\nFinal Results:")
    print("Roll Number:", roll_number if roll_number else "NOT FOUND")
    if not subjects_df.empty:
        print(subjects_df.to_csv(index=False))
    else:
        print("No subjects extracted.")
