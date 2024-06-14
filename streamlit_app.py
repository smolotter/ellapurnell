import streamlit as st


import subprocess
import tempfile

def html_to_pdf(html_file_path):
    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file.close()

    command = [
        "google-chrome-stable",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--print-to-pdf=" + pdf_file.name,
        html_file_path,
     ]

     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     process.communicate()

     return pdf_file_path