import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os
from collections import OrderedDict
import PyPDF2
import PyPDF2

st.title("ZIP to PDF Converter")

# Accept 4 zip files
zip_1 = st.file_uploader("Upload ZIP File 1", type="zip")
zip_2 = st.file_uploader("Upload ZIP File 2", type="zip")
zip_3 = st.file_uploader("Upload ZIP File 3", type="zip")
zip_4 = st.file_uploader("Upload ZIP File 4", type="zip")


def html_to_pdf(html_file_path):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()

    command = [
        "chromium",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--print-to-pdf=" + pdf_file.name,
        html_file_path,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file.name

def unzip_and_pdf(zip_obj, comp_name):

    st.write(f"Processing {comp_name}")

    zip_data = zip_obj.read()
    folder_name = zip_obj.name # Use the name of the uploaded file as the destination folder

    # Unzip the file
    with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
        zip_ref.extractall(folder_name)
                
        st.write(f"contents of {foldername}")
        st.json(zip_ref.namelist())

    # Get list of files in the directory (this only looks at the parent directory, not the subdirectories.)
    files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
    st.write("... interating through files in parent directory")
    st.json(files)

    for file in files:
        if file.endswith(".html"):  # Check if filename ends with ".html"
            st.write(f"...... processing {file}")
            pdf_path = html_to_pdf(folder_name + "/" + file)
            st.write(f"...... pdf path is {pdf_path}")
            pdf_files[comp_name + "_" + file.replace(".html",".pdf")] = pdf_path


pdf_files = OrderedDict() # To maintain insertion order, use this rather than a normal dictionary
if zip_1:
    unzip_and_pdf(zip_1, "covernote")
if zip_2:
    unzip_and_pdf(zip_2, "body")
if zip_3:
    unzip_and_pdf(zip_3, "annex")
if zip_4:
    unzip_and_pdf(zip_4, "distlist")


# This is just for debugging...
st.write(f"Individual pdf files created:")
st.json(pdf_files)
for pdf_name, pdf_path in pdf_files.items():
    st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)


list_A4 = []
list_SMC = []


# Filter based on key presence and absence of "SMC" 
for key, value in pdf_files.items():
    if "index.pdf" in key and "SMC_index.pdf" not in key:
        list_A4.append(value)
    elif "SMC_index.pdf" in key:
        list_SMC.append(value)


st.write("A4 pdfs:")
st.json(list_A4)
st.write ("SMC pdfs:")
st.json(list_SMC)


def combine_pdfs(pdf_files):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    merger = PyPDF2.PdfWriter()

    for pdf in pdf_files:
        merger.append(pdf)

    merger.write(temp_file)
    merger.close()
    return temp_file.name


combined_A4 = combine_pdfs(list_A4)
combined_SMC = combine_pdfs(list_SMC)

st.download_button(label="combined_A4.pdf", data=open(combined_A4, 'rb').read(), file_name="combined_A4.pdf")
st.download_button(label="combined_SMC.pdf", data=open(combined_SMC, 'rb').read(), file_name="combined_SMC.pdf")

