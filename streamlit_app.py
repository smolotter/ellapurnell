import streamlit as st
import zipfile
from io import BytesIO
import subprocess
import tempfile
import os


def html_to_pdf(html_file_path):
    print ("code failing1")
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
    print ("code failing2")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

    return pdf_file.name


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
        
        st.write (f"... unzipped {list_of_files}")

    # Get list of files in the directory
    files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]

    # Print the list of files
    for file in files:
        print(file)




if zip_1:
    st.write ("Processing Zip 1 ...")
    folder_name = unzip_to_folder(zip_1)




# if uploaded_zip is not None:
#     zip_data = uploaded_zip.read()

#     with zipfile.ZipFile(BytesIO(zip_data), 'r') as zip_ref:
#         extracted_files = {}  # Dictionary to store extracted files
#         for filename in zip_ref.namelist():
#             # Extract all files (HTML and CSS)
#             extracted_files[filename] = zip_ref.read(filename)

#     pdf_files = {}
#     for filename, file_content in extracted_files.items():
#         if filename.endswith(".html"):
#             # Process only HTML files for conversion
#             # Create temporary file and write HTML content
#             temp_html_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
#             temp_html_file.write(file_content)
#             temp_html_file.close()

#             # Convert HTML to PDF, ensuring proper path is passed
#             pdf_path = html_to_pdf(temp_html_file.name)

#             # Add PDF details to dictionary
#             pdf_files[filename[:-5] + ".pdf"] = pdf_path

#     # Display download buttons for each PDF
#     for pdf_name, pdf_path in pdf_files.items():
#         st.download_button(label=pdf_name, data=open(pdf_path, 'rb').read(), file_name=pdf_name)









