import os
import subprocess
import zipfile
import tempfile
from io import BytesIO
from datetime import datetime

import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PyPDF2 import PdfReader, PdfWriter


def unzip_file(stfileuploader, destination):
    """
    Unzip a file uploaded through Streamlit's file uploader and extract its contents to a specified destination.

    Parameters:
    - stfileuploader (UploadedFile): The file uploaded through Streamlit's file uploader.
    - destination (str): The directory path where the contents of the ZIP file will be extracted.

    Returns:
    - destination (str)
    """
    with zipfile.ZipFile(BytesIO(stfileuploader.read()), 'r') as zip_ref:
        zip_ref.extractall(destination)
    return destination

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


def add_header_footer(input_path, output_path, pdt_classification, pdt_docid, fontsz_classification, fontsz_others, margin_top, margin_right, margin_bottom, margin_left):
    """
    Add header and footer to an existing PDF document.

    Parameters:
    - input_path (str): Path to the input PDF file.
    - output_path (str): Path to save the output PDF file with headers and footers.
    - pdt_classification (str): Text for the classification to be displayed in the header and footer.
    - pdt_docid (str): Text for the document id to be displayed in the header.
    - fontsz_classification (int): Font size for the classification text, in points.
    - fontsz_others (int): Font size for the document id and page number text, in points
    - margin_top (float): Top margin for the header, in points.
    - margin_right (float): Right margin for the header and footer, in points.
    - margin_bottom (float): Bottom margin for the footer, in points.
    - margin_left (float): Left margin for the header, in points.

    Returns:
    - output_path (str): Path to the output PDF file with added headers and footers.
    """
    # Create a writer instance
    writer = PdfWriter()
    
    # Read the input PDF
    reader = PdfReader(input_path)
    width = reader.pages[0].mediabox.width  # Width in pts of the input
    height = reader.pages[0].mediabox.height  # Height in pts of the input
    num_pages = len(reader.pages)  # Number of pages of the input
    
    # Create a temporary PDF to hold the additional texts
    temp_pdf_path = "temp_headerfooter.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # Every page is different because of the page number
    for i in range(num_pages):
        # Start a new page in the temporary PDF
        c.showPage()

        # Draw classification in middle of header/footer
        c.setFont("Helvetica", fontsz_classification)

        c.drawCentredString(width / 2, 
                            height - margin_top,
                            pdt_classification)  # Header

        c.drawCentredString(width / 2, 
                            margin_bottom,
                            pdt_classification)  # Footer

        # Draw docid and page number in header
        c.setFont("Helvetica", fontsz_others)
        
        c.drawString(margin_left, 
                     height - margin_top - fontsz_classification,
                     pdt_docid)  # Docid

        c.drawRightString(width - margin_right,
                          height - margin_top - fontsz_classification,
                          str(i + 1))  # Page number

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
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    return output_path






st.title("ZIP to PDF Converter")

# Accept 4 zip files
zip_1 = st.file_uploader("Upload Covernote (if any)", type="zip")
zip_2 = st.file_uploader("Upload Main Product", type="zip")
zip_3 = st.file_uploader("Upload Annex (if any)", type="zip")
zip_4 = st.file_uploader("Upload Distriubtion List", type="zip")

# Placeholder
pdt_classification = "TOP SECRET & CILANTRO"
pdt_docid = "AB/123/2023"

# Create lists to hold individual pdfs
list_A4 = []
list_SMC = []
    
    ### TODO: add the coverpg

# Create a temp_dir to work in
with tempfile.TemporaryDirectory() as temp_dir, st.spinner('Processing...'):

    # Change the current working directory to temp_dir
    os.chdir(temp_dir)

    # Iterate through the uploaded zip files
    zip_files = [zip_1, zip_2, zip_3, zip_4]
    for i, zip_file in enumerate(zip_files, 1):
        if zip_file:

            # Unzip them
            unzipped = unzip_file(stfileuploader=zip_file, destination=f"unzipped_{i}")
            
            # Look for the html files, convert to pdf, and append them to a list for processing in the next step
            A4_pdf = html_to_pdf(html_path=os.path.join(unzipped, "index.html"), pdf_path=f"A4_{i}.pdf")
            list_A4.append(A4_pdf)
            
            SMC_pdf = html_to_pdf(html_path=os.path.join(unzipped, "SMC_index.html"), pdf_path=f"SMC_{i}.pdf")
            list_SMC.append(SMC_pdf)

    # Combine the PDFs and add header/footer
    if zip_2: #and other conditions such as the families

        # Combine the PDFs
        A4_C = combine_pdfs(list_of_individual_files = list_A4, output_path = "A4_C.pdf")
        SMC_C = combine_pdfs(list_of_individual_files = list_SMC, output_path = "SMC_C.pdf")

        # Add header and footer
        A4_O = add_header_footer(input_path = A4_C, 
                                output_path = "A4_O.pdf", 
                                pdt_classification = pdt_classification, 
                                pdt_docid = pdt_docid, 
                                fontsz_classification = 15, 
                                fontsz_others = 12, 
                                margin_top = 1 * cm, 
                                margin_right = 2.54 * cm, 
                                margin_bottom = 1 * cm, 
                                margin_left = 2.54 * cm,
                                )
        
        SMC_O = add_header_footer(input_path = SMC_C,
                                output_path = "SMC_O.pdf", 
                                pdt_classification = pdt_classification, 
                                pdt_docid = pdt_docid, 
                                fontsz_classification = 14, 
                                fontsz_others = 10, 
                                margin_top = 0.5 * cm, 
                                margin_right = 1 * cm, 
                                margin_bottom = -1, # Place off page, since smc version doesnt have this
                                margin_left = 1 * cm,
                                )        

        try:
            st.info("Wait for processing to be complete before downloading!")
            st.header("Output files:")
            st.download_button(label="A4 output", data=open(A4_O, 'rb').read(), file_name=pdt_docid + " (A4) " + datetime.now().strftime("(%d %b %Y %H%M)"))
            st.download_button(label="SMC output", data=open(SMC_O, 'rb').read(), file_name=pdt_docid + " (SMC) " + datetime.now().strftime("(%d %b %Y %H%M)"))
        except:
            st.error("Something went wrong, the output could not be presented.")



    with st.expander("For debugging"):
        # For debugging
        st.header(f"Intermediate files:")
        filenames = ["A4_1.pdf", "SMC_1.pdf",
                    "A4_2.pdf", "SMC_2.pdf",
                    "A4_3.pdf", "SMC_3.pdf",
                    "A4_4.pdf", "SMC_4.pdf",
                    "A4_C.pdf", "SMC_C.pdf",
                    "A4_O.pdf", "SMC_O.pdf",
                    ]
        for filename in filenames:
            try:
                st.download_button(label=filename, data=open(os.path.join(temp_dir, filename), 'rb').read(), file_name=filename)
            except:
                st.write(f"{filename} not exist")

        os.chdir('/')
        st.header(f"Debug: contents of '{temp_dir}':")
        st.json(os.listdir(temp_dir))

        st.header(f"Debug: contents of '/':")
        st.json(os.listdir('/'))

        directory_path = st.text_input("Enter the directory path:")
        if directory_path:
            st.header(f"Debug: contents of '{directory_path}':")
            st.json(os.listdir(directory_path))


