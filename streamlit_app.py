import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os
from collections import OrderedDict
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

    st.write(f"... unzipping {folder_name}")

    # Unzip the file
    with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
        zip_ref.extractall(folder_name)
        list_of_files = zip_ref.namelist()
        
        st.write(f"... unzipped {list_of_files}")

    # Get list of files in the directory (this only looks at the parent directory, not the subdirectories.)
    files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
    st.write(f"... looking for html files in parent directory: {files}")

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




def concatenate_pdfs(pdf_files, output_filename):
    """Concatenates multiple PDF files into a single output PDF.

    Args:
        pdf_files (list): A list of file paths of the PDFs to concatenate.
        output_filename (str): The filename of the resulting concatenated PDF.
    """

    pdf_reader_list = []
    for filename in pdf_files:
        with open(filename, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_reader_list.append(pdf_reader)

    pdf_writer = PyPDF2.PdfWriter()

    for pdf_reader in pdf_reader_list:
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.pages[page_num]
            pdf_writer.addPage(page)

    with open(output_filename, 'wb') as output_file:
        pdf_writer.write(output_file)

# Example usage
pdf_files = [
    "path/to/file1.pdf",
    "path/to/file2.pdf",
    "path/to/file3.pdf",
    # ...
]
output_filename = "merged_output.pdf"

concatenate_pdfs(pdf_files, output_filename)

print(f"PDFs concatenated successfully! Output file: {output_filename}")



