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
st.write("version 305")

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



from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def add_header_footer(path_to_input, pdt_classification, doc_id, path_to_output):
    """
    Adds a header and footer to a PDF file using ReportLab, handling multiple pages.

    Args:
        path_to_input: Path to the input PDF file.
        pdt_classification: String representing the PDF classification.
        doc_id: String representing the document ID.
        path_to_output: Path to save the modified PDF file.

    Returns:
        str: Path to the output PDF file.
    """
    # Define styles for header and footer content
    styles = getSampleStyleSheet()

    def header(canvas, doc):
        # Create header content
        header_text = f"{doc_id} - {pdt_classification} - Page {doc.page + 1}"
        content = Paragraph(header_text, styles['Normal'])
        # Set header position (adjust as needed)
        content.wrapOn(doc, A4[0], A4[1])  # Wrap content within page size
        content.drawOn(canvas, 50, doc.height - 20)  # Draw header with margins

    def footer(canvas, doc):
        # Create footer content
        footer_text = f"{pdt_classification}"
        content = Paragraph(footer_text, styles['Normal'])
        # Set footer position (adjust as needed)
        content.wrapOn(doc, A4[0], A4[1])  # Wrap content within page size
        content.drawOn(canvas, 50, 20)  # Draw footer with margins

    # Build the document with header and footer functions
    doc = SimpleDocTemplate(filename=path_to_output, pagesize=A4)
    template = PageTemplate(id='all', frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main')], onPage=header + footer)
    doc.addPageTemplates([template])

    # Reference content from original PDF (iterating through pages)
    elements = []
    with open(path_to_input, 'rb') as input_file:
        for page_num in range(1, input_file.read().count(b"/Contents") + 1):  # Count page objects
            elements.append(Spacer(1, A4[1] - doc.topMargin - doc.bottomMargin))  # Spacer for content
            elements.append(input_file.seek(0, io.SEEK_SET))  # Reset file pointer for each page
            elements.append(input_file.read(input_file.read().find(b"endstream") + len(b"endstream")))  # Read each page content

    doc.build(elements)

    return path_to_output




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


    # Combine the PDFs

    A4_C = combine_pdfs(list_of_individual_files = list_A4,
                        output_file_path = os.path.join(temp_dir, "A4_C.pdf")
                        )
    
    SMC_C = combine_pdfs(list_of_individual_files = list_SMC,
                        output_file_path = os.path.join(temp_dir, "SMC_C.pdf")
                        )


    # Add header and footer
    
    pdt_classification = "TOP SECRET & CILANTRO"
    doc_id = "DOCID/PLACEHOLDER"

    A4_HF = add_header_footer(path_to_input=A4_C,
                              pdt_classification = pdt_classification,
                              doc_id = doc_id,
                              path_to_output = os.path.join(temp_dir, "A4_HF.pdf")
                              
    SMC_HF = add_header_footer(path_to_input=A4_C,
                              pdt_classification = pdt_classification,
                              doc_id = doc_id,
                              path_to_output = os.path.join(temp_dir, "SMC_HF.pdf")




    # TODO: add the coverpg


    # For debugging
    filenames = ["A4_1.pdf", "SMC_1.pdf",
                 "A4_2.pdf", "SMC_2.pdf",
                 "A4_3.pdf", "SMC_3.pdf",
                 "A4_4.pdf", "SMC_4.pdf",
                 "A4_C.pdf", "SMC_C.pdf",
                 "A4_HF.pdf", "SMC_HF.pdf",
                 "A4_O.pdf", "SMC_O.pdf",
                 ]
    for filename in filenames:
        try:
            st.download_button(label=filename, data=open(os.path.join(temp_dir, filename), 'rb').read(), file_name=filename)
        except:
            st.write(f"{filename} not exist")



    
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
