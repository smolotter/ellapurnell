import os
import zipfile
import tempfile
import subprocess
from PyPDF2 import PdfWriter, PdfReader
import streamlit as st

import shutil


def html_to_pdf(html_path, pdf_path):
    """
    Converts an HTML file to PDF using Chromium.

    Parameters:
    - html_path (str): Path to the HTML file to be converted.
    - pdf_path (str): Path where the generated PDF will be saved.

    Returns:
    - pdf_path (str)
    """
    command = [
        "chromium",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + pdf_path,
        html_path,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        st.error(f"Error converting HTML to PDF: {error.decode()}")
    return pdf_path


def main():
    st.title("Dynamic File Uploader and PDF Combiner")

    # Create a dropdown menu with options from 1 to 50
    st.markdown("**How many zip files do you have?**")
    with st.expander("Click here to see examples"):
        st.write("The minimum is 2: One product body + One distribution list.")
        # ... (rest of explanation)

    num_files = st.selectbox("Select Number of Files", range(2, 51))

    # Create a list to store the uploaded files
    uploaded_files = []

    # Create the appropriate number of file upload boxes
    for i in range(num_files):
        uploaded_file = st.file_uploader(f"Upload File {i+1}")
        uploaded_files.append(uploaded_file)

    if uploaded_files:
        # List to store paths of all PDF files
        
        # Create a temporary directory to extract the zip file
        with tempfile.TemporaryDirectory() as temp_dir:

            pdf_files_hc = []
            pdf_files_smc = []
            temp_dir_pdf = "temp_dir" + "/pdf"

            for i, file in enumerate(uploaded_files):

                temp_dir_num = "temp_dir" + "/" + str(i + 1)
                st.write (temp_dir_num)
                if file is not None:
                    st.write(f"File {i+1}: {file.name}")

                    # Extract the zip file to the temporary directory
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir_num)

                    for item in os.listdir(temp_dir):
                        st.write(item)


            #         # Iterate through each file in the unzipped directory
            #         for root, dirs, files in os.walk(temp_dir):
            #             for file in files:
            #                 if file.endswith(".html"):
            #                     html_path = os.path.join(root, file)
            #                     pdf_path = os.path.join(root, file[:-5] + ".pdf")
            #                     html_to_pdf(html_path, pdf_path)
            #                 elif file.endswith(".pdf"):
            #                     pdf_files.append(os.path.join(root, file))
                    
            # # Combine PDF files
            # merger = PdfWriter()
            # for pdf_file in pdf_files:
            #     with open(pdf_file, "rb") as f:
            #         pdf_reader = PdfReader(f)
            #         for page_num in range(len(pdf_reader.pages)):
            #             page = pdf_reader.pages[page_num]
            #             merger.add_page(page)

            # output_path = os.path.join(temp_dir, "combined.pdf")
            # merger.write(output_path)

            # # Download the combined PDF
            # with open(output_path, 'rb') as f:
            #     st.download_button(
            #         label="Download Combined PDF",
            #         data=f,
            #         file_name="combined.pdf",
            #         mime='application/pdf'
            #     )

if __name__ == "__main__":
    main()