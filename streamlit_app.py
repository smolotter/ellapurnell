import os
import zipfile
import tempfile
import subprocess
from PyPDF2 import PdfWriter, PdfReader
import streamlit as st
import shutil

def html_to_pdf(html_path, pdf_path):
    # ... (your existing html_to_pdf function)

def main():
    st.title("Dynamic File Uploader and PDF Combiner")

    # ... (rest of your code for selecting files and unzipping)

    if uploaded_files:
        for i, file in enumerate(uploaded_files):
            if file is not None:
                # ... (rest of your code for unzipping the file)

                # List to store paths of all PDF files
                pdf_files = []

                # Iterate through each file in the unzipped directory
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".html"):
                            html_path = os.path.join(root, file)
                            pdf_path = os.path.join(root, file[:-5] + ".pdf")
                            html_to_pdf(html_path, pdf_path)
                        elif file.endswith(".pdf"):
                            pdf_files.append(os.path.join(root, file))

                # Combine PDF files
                merger = PdfWriter()
                for pdf_file in pdf_files:
                    with open(pdf_file, "rb") as f:
                        pdf_reader = PdfReader(f)
                        for page_num in range(len(pdf_reader.pages)):
                            page = pdf_reader.pages[page_num]
                            merger.add_page(page)

                output_path = os.path.join(temp_dir, "combined.pdf")
                merger.write(output_path)

                # Download the combined PDF
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="Download Combined PDF",
                        data=f,
                        file_name="combined.pdf",
                        mime='application/pdf'
                    )

                # Clean up the temporary directory
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()