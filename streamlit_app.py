import streamlit as st
import zipfile
from io import BytesIO
import tempfile

def html_to_pdf(html_file_path):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()

    command = [
        "chromium",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--print-to-pdf=" + pdf_file.name,
        html_file_path,
     ]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file.name

st.title("HTML to PDF Converter")

uploaded_zip = st.file_uploader("Upload ZIP file")

if uploaded_zip is not None:
    zip_data = uploaded_zip.read()

    with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
        extracted_files = {}  # Dictionary to store extracted files
        for filename in zip_ref.namelist():
            # Extract all files (HTML and CSS)
            extracted_files[filename] = zip_ref.read(filename)

    pdf_files = {}
    for filename, file_content in extracted_files.items():
        if filename.endswith(".html"):
            # Process only HTML files for conversion
            # Create temporary file and write HTML content
            temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            temp_html_file.write(file_content)
            temp_html_file.close()

            # Convert HTML to PDF, ensuring proper path is passed
            pdf_path = html_to_pdf(temp_html_file.name)

            # Add PDF details to dictionary
            pdf_files[filename[:-5] + ".pdf"] = pdf_path

    # Display download buttons for each PDF
    for pdf_name, pdf_path in pdf_files.items():
        st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)
