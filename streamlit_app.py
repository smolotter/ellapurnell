import streamlit as st


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

@st.cache_resource
def get_driver():
    return webdriver.Chrome(
        service=Service(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        ),
        options=options,
    )

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--headless")

driver = get_driver()
# driver.get("http://example.com")


 
 

import os
from pyhtml2pdf import converter
# path = os.path.abspath('index.html')
# converter.convert(f'file:///{path}', 'sample.pdf') #local file

converter.convert('https://pypi.org', 'sample.pdf') #web based


with open("sample.pdf", "rb") as pdf_file:
    data = pdf_file.read()
st.download_button("Download sample.pdf", data=data, file_name="sample.pdf")