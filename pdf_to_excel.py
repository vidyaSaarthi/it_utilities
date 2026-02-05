import pdfplumber
import pandas as pd

# Input/output file paths
location  = r"C:\Users\Shubham Aggarwal\Downloads\\"
pdf_file_only_name='Open Round Seat Position'
pdf_path = location + pdf_file_only_name + ".pdf"
excel_path = location + pdf_file_only_name + '.csv'

combined_data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table[1:], columns=table[0])  # Use first row as headers
            combined_data.append(df)

# Combine all pages into one DataFrame
if combined_data:
    full_df = pd.concat(combined_data, ignore_index=True)
    full_df.to_csv(excel_path, index=False)
    print(f"Excel saved to: {excel_path}")
else:
    print("No tables found in PDF.")
