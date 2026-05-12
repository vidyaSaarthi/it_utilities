from docx import Document
import re
import json

def extract_sections(docx_path):
    doc = Document(docx_path)

    sections = {}
    current_heading = None
    content_buffer = []

    # Pattern to detect headings like:
    # "1. College Images & Visuals"
    heading_pattern = re.compile(r'^\d+\.\s+.+')

    started = False  # To skip initial prompt

    for para in doc.paragraphs:
        text = para.text.strip()

        if not text:
            continue

        # Start after first heading appears
        if heading_pattern.match(text):
            started = True

        if not started:
            continue

        # If it's a heading
        if heading_pattern.match(text):
            if current_heading:
                sections[current_heading] = "\n".join(content_buffer).strip()

            current_heading = text
            content_buffer = []

        else:
            content_buffer.append(text)

    # Save last section
    if current_heading:
        sections[current_heading] = "\n".join(content_buffer).strip()

    return sections


# Example usage
data = extract_sections(r"C:\Users\Shubham Aggarwal\Downloads\RIMS, Ongole , BHAGYANAGAR 5TH LANE, RIMS, ONGOLE,.docx")

# Save to JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)