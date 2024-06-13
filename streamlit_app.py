from seleniumprint import file_to_pdf

input_html_file_path="/Users/user/path/to/input.html"
output_pdf_file_path="/Users/user/path/to/output.pdf"

file_to_pdf(input_html_file_path, output_pdf_file_path)

input_html_url="http://localhost:8000/report/1"
output_pdf_file_path="./report_pdfs/report_1.pdf"

url_to_pdf(input_html_url, output_pdf_file_path)