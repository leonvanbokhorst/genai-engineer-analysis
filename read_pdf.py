import fitz  # PyMuPDF
import os

# Define file paths
pdf_path = os.path.join("data", "CAIN2022.pdf")
output_txt_path = os.path.join("data", "CAIN2022.txt")

# Check if the PDF file exists
if not os.path.exists(pdf_path):
    print(f"Error: The file '{pdf_path}' was not found.")
else:
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)

        # Initialize an empty string to hold the text
        full_text = ""

        # Loop through each page and extract text
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text()
            full_text += "\n--- End of Page ---\n"

        # Save the extracted text to a .txt file
        with open(output_txt_path, "w", encoding="utf-8") as text_file:
            text_file.write(full_text)

        print(f"Successfully extracted text from '{pdf_path}'")
        print(f"Full text saved to '{output_txt_path}'")

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
