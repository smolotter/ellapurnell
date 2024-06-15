import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os
from collections import OrderedDict
from PyPDF2 import PdfWriter
import time
import uuid



st.title("ZIP to PDF Converter")

# Create a UUID
session_uuid = str(uuid.uuid4())


# Accept 4 zip files
zip_1 = st.file_uploader("Upload Covernote (if any)", type="zip")
zip_2 = st.file_uploader("Upload Main Product", type="zip")
zip_3 = st.file_uploader("Upload Annex (if any)", type="zip")
zip_4 = st.file_uploader("Upload Distriubtion List", type="zip")






def unzip_file(stfileuploader, component_name, temp_dir=temp_dir):
    ''' Unzips a file (stfileuploader, from st.file_uploader), to a destination (temp_dir/component_name) '''
    destination = os.path.join(temp_dir, component_name)
    with zipfile.ZipFile(BytesIO(stfileuploader.read()), 'r') as zip_ref:
        zip_ref.extractall(destination)

    return destination

def html_to_pdf(html_file_path):
    ''' Converts a html file to a pdf file. Takes in a html file path, returns a pdf (temp) file path. Requires chromium.'''
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


def unzip_and_pdf(folder_name, component_name, temp_dir=temp_dir):
    ''' Iterate through a folder and pdf the zip files'''
    files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))] # Only in the main folder, not in subdirectories!

    for file in files:
        if file.endswith(".html"):  # Check if filename ends with ".html"
            pdf_path = html_to_pdf(folder_name + "/" + file)
            individual_pdf_files[comp_name + "_" + file.replace(".html",".pdf")] = pdf_path




# Create a temp_dir to work in
with tempfile.TemporaryDirectory() as temp_dir:

    # Create working files
    filenames = ["A4_1.pdf", "SMC_1.pdf",
                 "A4_2.pdf", "SMC_2.pdf",
                 "A4_3.pdf", "SMC_3.pdf",
                 "A4_4.pdf", "SMC_4.pdf",
                 "A4_C.pdf", "SMC_C.pdf",
                 "A4_O.pdf", "SMC_O.pdf",
                 ]
    for filename in filenames:
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, 'wb') as f:  # Use 'wb' for binary data
            pass  # Empty file creation

    # Create working dictionary and lists
    individual_pdf_files = OrderedDict() # To maintain insertion order, use this rather than a normal dictionary    
    list_A4 = []
    list_SMC = []

    # Iterate through the uploaded zip files
    
    if zip_1:
        unzipped_1 = unzip(stfileuploader = zip_1, component = "1", temp_dir = temp_dir)
    if zip_2:
        unzipped_2 = unzip(stfileuploader = zip_2, component = "2", temp_dir = temp_dir)
    if zip_3:
        unzipped_3 = unzip(stfileuploader = zip_3, component = "3", temp_dir = temp_dir)
    if zip_4:
        unzipped_4 = unzip(stfileuploader = zip_4, component = "4", temp_dir = temp_dir)


# For debugging
st.write(f"Individual pdf files...")
st.json(individual_pdf_files)
for pdf_name, pdf_path in individual_pdf_files.items():
    st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)


# Filter based on key presence and absence of "SMC" 

for key, value in individual_pdf_files.items():
    if "index.pdf" in key and "SMC_index.pdf" not in key:
        list_A4.append(value)
    elif "SMC_index.pdf" in key:
        list_SMC.append(value)


# For debugging
st.write("Sorted into A4 and SMC pdfs...")
st.write(f"...A4 pdfs is {list_A4}")
st.write (f"...SMC pdfs is {list_SMC}")


# Combine the PDFs
def combine_pdfs(individual_pdf_files):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    merger = PdfWriter()

    for pdf in individual_pdf_files:
        merger.append(pdf)

    merger.write(temp_file)
    merger.close()
    return temp_file.name

combined_A4 = combine_pdfs(list_A4)
combined_SMC = combine_pdfs(list_SMC)


# For debugging
st.write("Combined PDFs...")
st.download_button(label="combined_A4.pdf", data=open(combined_A4, 'rb').read(), file_name="combined_A4.pdf")
st.download_button(label="combined_SMC.pdf", data=open(combined_SMC, 'rb').read(), file_name="combined_SMC.pdf")






import os

def get_folder_size(path):
  """
  Calculates the total size of a directory and its subdirectories.

  Args:
      path: The path to the directory.

  Returns:
      The total size of the directory in bytes.
  """
  total_size = 0
  for root, _, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      try:
        total_size += os.path.getsize(file_path)
      except OSError:
        # Handle potential permission errors or other issues
        pass
  return total_size

# Example usage
folder_path = "/tmp"
folder_size = get_folder_size(folder_path)

# Convert to human-readable format (optional)
if folder_size > 1024**3:
  folder_size = folder_size / (1024**3)
  unit = "GB"
elif folder_size > 1024**2:
  folder_size = folder_size / (1024**2)
  unit = "MB"
elif folder_size > 1024:
  folder_size = folder_size / 1024
  unit = "KB"
else:
  unit = "bytes"

st.write(f"Total size of folder '{folder_path}': {folder_size:.2f} {unit}")



st.write("check tmp contents")
st.write(os.listdir("/tmp"))
