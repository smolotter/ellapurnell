import streamlit as st
import zipfile
from io import BytesIO
import tempfile

def html_to_pdf(html_file_path):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()

    command = [
        "chromium",  # Replace with "google-chrome-stable" if needed
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

uploaded_file = st.file_uploader("Upload HTML file")

if uploaded_file is not None:
    # Read uploaded file content
    html_content = uploaded_file.read().decode("utf-8")

    # Create temporary HTML file
    temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    temp_html_file.write(html_content.encode("utf-8"))
    temp_html_file.close()

    # Convert HTML to PDF
    pdf_path = html_to_pdf(temp_html_file.name)

    # Offer download link for the PDF
    st.download_button(label="Download PDF", data=open(pdf_path, 'rb').read(), file_name="converted.pdf")
