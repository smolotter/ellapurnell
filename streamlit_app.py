import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os


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
        "--print-to-pdf=" + pdf_file.name,
        html_file_path,
    ]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file.name
    


def unzip_to_folder(zip_obj): #Unzip the object uploaded in streamlit

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
    st.write(f"... looking for html files in {files}")

    for file in files:
        if file.endswith(".html"):  # Check if filename ends with ".html"
            st.write(f"... processing {file}")
            pdf_path = html_to_pdf(file)
            st.write(pdf_path)
            pdf_files[filename[:-5] + ".pdf"] = pdf_path


pdf_files = {}
if zip_1:
    st.write ("Processing Zip 1 ...")
    folder_name = unzip_to_folder(zip_1)



# for pdf_name, pdf_path in pdf_files.items():
#     st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)









