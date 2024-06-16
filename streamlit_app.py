import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os
from collections import OrderedDict
from PyPDF2 import PdfWriter
import time

st.title("ZIP to PDF Converter")
st.write("version 955")

def unzip_file(stfileuploader, component, temp_dir):
    ''' Unzips a file (stfileuploader, from st.file_uploader), to a destination (temp_dir/component) '''
    destination = os.path.join(temp_dir, component)
    with zipfile.ZipFile(BytesIO(stfileuploader.read()), 'r') as zip_ref:
        zip_ref.extractall(destination)

    return destination

def html_to_pdf(html_file_path, pdf_file_path):
    """Converts an HTML file to PDF using Chromium."""
    command = [
                "chromium",
                "--headless",
                "--no-sandbox",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--print-to-pdf=" + pdf_file_path,
                html_file_path,
                ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file_path

def combine_pdfs(list_of_individual_files, output_file_path):
    """Combines a list of PDFs into a single PDF."""
    merger = PdfWriter()

    for pdf in list_of_individual_files:
        merger.append(pdf)

    merger.write(output_file_path)
    merger.close()

    return output_file_path

import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Function to convert points to centimeters
def points_to_cm(points):
    return points * 2.54 / 72

def cm_in_points(cm):
    return cm * 72 / 2.54

def add_page_numbers_and_classification(input_pdf_path, output_pdf_path):
    
    # Create a writer instance
    writer = PdfWriter()
    
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    width = reader.pages[0].mediabox.width # Width in pts of the input
    height = reader.pages[0].mediabox.height # Height in pts of the input
    num_pages = len(reader.pages) # Number of pages of the input
    
    # Create a temporary PDF to hold the additional texts
    temp_pdf_path = "temp_headerfooter.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # Every page is different because of the page number
    for i in range(num_pages):
        # Start a new page in the temporary PDF
        c.showPage()

        # Draw docid and page number in header
        c.setFont("Helvetica", 12)
        
        c.drawString(cm_in_points(2.54), 
                     height - cm_in_points(1.5),
                     "doc_id_placeholder") # Docid

        c.drawRightString(width - cm_in_points(2.54),
                          height - cm_in_points(1.5), 
                          str(i + 1)) # Page number

        # Draw classification in middle of header/footer
        c.setFont("Helvetica", 16)

        c.drawCentredString(width / 2, 
                            height - cm_in_points(1),
                            "classification") # Header

        c.drawCentredString(width / 2, 
                            cm_in_points(1),
                            "classification") # Footer
    
    c.save()
    
    # Read the temporary PDF with the additional texts
    temp_reader = PdfReader(temp_pdf_path)
    
    # Merge the temporary PDF with the original PDF
    for i in range(num_pages):
        # Get the original page
        original_page = reader.pages[i]
        # Get the additional texts overlay
        additional_texts_overlay = temp_reader.pages[i]
        # Merge the two pages
        original_page.merge_page(additional_texts_overlay)
        # Add the merged page to the writer
        writer.add_page(original_page)
    
    # Write the final PDF to the output path
    with open(output_pdf_path, "wb") as output_pdf_file:
        writer.write(output_pdf_file)

    return output_pdf_file

# Create a temp_dir to work in
with tempfile.TemporaryDirectory() as temp_dir:


    # Accept 4 zip files
    zip_1 = st.file_uploader("Upload Covernote (if any)", type="zip")
    zip_2 = st.file_uploader("Upload Main Product", type="zip")
    zip_3 = st.file_uploader("Upload Annex (if any)", type="zip")
    zip_4 = st.file_uploader("Upload Distriubtion List", type="zip")

    # Create lists to hold individual pdfs
    list_A4 = []
    list_SMC = []

    # TODO: add the coverpg

    # Iterate through the uploaded zip files
    if zip_1:

        unzipped_1 = unzip_file(stfileuploader = zip_1, component = "1", temp_dir = temp_dir)
        
        A4_1 = html_to_pdf(html_file_path = os.path.join(unzipped_1, "index.html"),
                    pdf_file_path = os.path.join(temp_dir, "A4_1.pdf")
                    )
        list_A4.append(A4_1)
        
        SMC_1 = html_to_pdf(html_file_path = os.path.join(unzipped_1, "SMC_index.html"),
                    pdf_file_path = os.path.join(temp_dir, "SMC_1.pdf")
                    )
        list_SMC.append(SMC_1)

    if zip_2:

        unzipped_2 = unzip_file(stfileuploader = zip_2, component = "2", temp_dir = temp_dir)
        
        A4_2 = html_to_pdf(html_file_path = os.path.join(unzipped_2, "index.html"),
                    pdf_file_path = os.path.join(temp_dir, "A4_2.pdf")
                    )
        list_A4.append(A4_2)
        
        SMC_2 = html_to_pdf(html_file_path = os.path.join(unzipped_2, "SMC_index.html"),
                    pdf_file_path = os.path.join(temp_dir, "SMC_2.pdf")
                    )
        list_SMC.append(SMC_2)

    if zip_3:
        
        unzipped_3 = unzip_file(stfileuploader = zip_3, component = "3", temp_dir = temp_dir)
        
        A4_3 = html_to_pdf(html_file_path = os.path.join(unzipped_3, "index.html"),
                    pdf_file_path = os.path.join(temp_dir, "A4_3.pdf")
                    )
        list_A4.append(A4_3)

        SMC_3 = html_to_pdf(html_file_path = os.path.join(unzipped_3, "SMC_index.html"),
                    pdf_file_path = os.path.join(temp_dir, "SMC_3.pdf")
                    )
        list_SMC.append(SMC_3)

    if zip_4:
        
        unzipped_4 = unzip_file(stfileuploader = zip_4, component = "4", temp_dir = temp_dir)

        A4_4 = html_to_pdf(html_file_path = os.path.join(unzipped_4, "index.html"),
                    pdf_file_path = os.path.join(temp_dir, "A4_4.pdf")
                    )
        list_A4.append(A4_4)

        SMC_4 = html_to_pdf(html_file_path = os.path.join(unzipped_4, "SMC_index.html"),
                    pdf_file_path = os.path.join(temp_dir, "SMC_4.pdf")
                    )
        list_SMC.append(SMC_4)


    if zip_2: #and other conditions such as the families

        # Combine the PDFs

        A4_C = combine_pdfs(list_of_individual_files = list_A4,
                            output_file_path = os.path.join(temp_dir, "A4_C.pdf")
                            )
        
        SMC_C = combine_pdfs(list_of_individual_files = list_SMC,
                            output_file_path = os.path.join(temp_dir, "SMC_C.pdf")
                            )


        # Add header and footer

        A4_O = add_page_numbers_and_classification(input_pdf_path = A4_C,
                                                output_pdf_path = os.path.join(temp_dir, "A4_O.pdf"))

        SMC_O = add_page_numbers_and_classification(input_pdf_path = SMC_C,
                                                output_pdf_path = os.path.join(temp_dir, "SMC_O.pdf"))
        

        # For debugging
        filenames = ["A4_1.pdf", "SMC_1.pdf",
                     "A4_2.pdf", "SMC_2.pdf",
                     "A4_3.pdf", "SMC_3.pdf",
                     "A4_4.pdf", "SMC_4.pdf",
                     "A4_C.pdf", "SMC_C.pdf",
                     "A4_O.pdf", "SMC_O.pdf",
                    ]
        st.header(f"For debugging:")
        for filename in filenames:
            try:
                st.download_button(label=filename, data=open(os.path.join(temp_dir, filename), 'rb').read(), file_name=filename)
            except:
                st.write(f"{filename} not exist")

    
    # For debugging
    st.header(f"Debug: contents of '{temp_dir}':")
    st.json(os.listdir(temp_dir))



    # For debugging
    directory_path = st.text_input("Enter the directory path:")
    if directory_path:
        st.header(f"Debug: contents of '{directory_path}':")
        st.json(os.listdir(directory_path))
    
    st.title("Directory Viewer")
    

    
# import uuid
# # Create a UUID
# session_uuid = str(uuid.uuid4())

# import os

# def get_folder_size(path):
#   """
#   Calculates the total size of a directory and its subdirectories.

#   Args:
#       path: The path to the directory.

#   Returns:
#       The total size of the directory in bytes.
#   """
#   total_size = 0
#   for root, _, files in os.walk(path):
#     for file in files:
#       file_path = os.path.join(root, file)
#       try:
#         total_size += os.path.getsize(file_path)
#       except OSError:
#         # Handle potential permission errors or other issues
#         pass
#   return total_size

# # Example usage
# folder_path = "/tmp"
# folder_size = get_folder_size(folder_path)

# # Convert to human-readable format (optional)
# if folder_size > 1024**3:
#   folder_size = folder_size / (1024**3)
#   unit = "GB"
# elif folder_size > 1024**2:
#   folder_size = folder_size / (1024**2)
#   unit = "MB"
# elif folder_size > 1024:
#   folder_size = folder_size / 1024
#   unit = "KB"
# else:
#   unit = "bytes"

# st.write(f"Total size of folder '{folder_path}': {folder_size:.2f} {unit}")



# st.write("check tmp contents")
# st.write(os.listdir("/tmp"))
