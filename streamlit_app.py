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
    process.communicate()

    return pdf_path

def combine_pdfs(list_of_individual_files, output_path):
    """
    Combines a list of PDFs into a single PDF.

    Parameters:
    - list_of_individual_files (list): List of paths to individual PDF files to be combined.
    - output_path (str): Path where the combined PDF will be saved.

    Returns:
    - output_path (str)
    """
    merger = PdfWriter()

    for pdf in list_of_individual_files:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()

    return output_path

def list_directory(directory):
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        st.write(item + ("/" if os.path.isdir(full_path) else ""))
        if os.path.isdir(full_path):
            list_directory(full_path)


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

            list_of_pdf_files_hc = []
            list_of_pdf_files_smc = []

            for i, file in enumerate(uploaded_files):

                if file is not None:
                    st.write(f"Processing file {i+1}: {file.name}")
                    path_of_dir = temp_dir + "/" + str(i + 1)

                    # Extract the zip file to the temporary directory
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_ref.extractall(path_of_dir)

                    path_of_index_html = path_of_dir + "/index.html"
                    path_of_pdf = path_of_dir + "/hc.pdf"
                    html_to_pdf(path_of_index_html, path_of_pdf)
                    list_of_pdf_files_hc.append(path_of_pdf)

                    path_of_SMC_index_html = path_of_dir + "/SMC_index.html"
                    path_of_pdf = path_of_dir + "/smc.pdf"
                    html_to_pdf(path_of_SMC_index_html, path_of_pdf)
                    list_of_pdf_files_smc.append(path_of_pdf)


            list_directory(temp_dir)




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