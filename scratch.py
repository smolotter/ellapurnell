from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm


def add_header_footer(input_path, output_path, pdf_classification):
    """
    Adds a header and footer to a multi-page PDF file

    Args:
        pdf_classification (str): String to display in the header.
        input_path (str): Path to the existing PDF file.
        output_path (str): Path to save the modified PDF file.
    """
    def footer_canvas(canvas, doc):
        """
        Function to draw the footer on each page.
        """
        page_num = canvas.getPageNumber()
        footer_text = "Page %d" % page_num
        canvas.setFont("Helvetica", 15)
        canvas.drawCentredString(9 * cm, 19 * cm, header_text)

    def header_canvas(canvas, doc):
        """
        Function to draw the header on each page.
        """
        header_text = "Classification: %s" % pdf_classification
        canvas.setFont("Helvetica", 15)
        canvas.drawCentredString(9 * cm, 19 * cm, header_text)

    def background_canvas(canvas, doc):
        """
        Function to draw a blank background for the existing content.
        """
        canvas.setStrokeColor(None)  # Remove stroke color
        canvas.setFillColor((255, 255, 255))  # Set white fill color
        canvas.drawRect(1.9 * cm, 1.9 * cm, 18 * cm, 21.5 * cm)  # Draw background rectangle
    
    styles = getSampleStyleSheet()

    # Read existing content
    existing_content = []
    with open(input_path, 'rb') as pdf_in:
        # Use platypus read to handle existing content
        existing_content = read(pdf_in)

    # Define a template with background and overlaying header/footer
    template = PageTemplate(
        id="MainTemplate",
        frames=[Frame(x1=0, y1=0, width=21 * cm, height=29.7 * cm)],  # Full page frame
        onPage=background_canvas,  # Draw background first
        onPageEnd=footer_canvas,
        onPageBegin=header_canvas,  # Overlays header and footer
        )

    # Build the new PDF with existing content and defined template
    SimpleDocTemplate(
        output_path,
        pagesize=existing_content[0].pagesize,  # Inherit page size
    ).build([template] + existing_content)

    return output_path

# Example usage
pdf_classification = "Confidential"
input_path = "original.pdf"
output_path = "modified.pdf"
add_header_footer(pdf_classification, input_path, output_path)




from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def add_header_footer(pdf_classification, input_file, output_file, page_size=(A4[0], A4[1])):
  """
  Adds header and footer to a multi-page PDF file.

  Args:
    pdf_classification (str): Text to display in the header.
    input_file (str): Path to the existing PDF file.
    output_file (str): Path to save the modified PDF file.
    page_size (tuple): Page size in centimeters (width, height). Defaults to A4.
  """
  # Define styles
  header_style = Paragraph(pdf_classification, fontSize=15 * cm, fontName="Helvetica")
  footer_style = Paragraph("Page %d" % canvas.page_number(), fontSize=15 * cm, fontName="Helvetica", alignment=canvas.RIGHT)

  def footer(canvas, doc):
    # Draw footer on every page
    canvas.saveState()
    footer_style.wrapOn(canvas, page_size[0], page_size[1] - 2 * cm)  # Adjust footer position
    footer_style.drawOn(canvas, *canvas._coord)
    canvas.restoreState()

  def myFirstPage(canvas, doc):
    # No content needed here as the header is drawn in drawOn

  # Open existing PDF and create a new one
  c = canvas.Canvas(output_file, pagesize=page_size)
  c.setViewerPreference(FitWindow=True)  # Maintain zoom on existing content

  # Process each page of the existing PDF
  pageCount = canvas.pageCount(input_file)
  for pageNo in range(1, pageCount + 1):
    template = c.BeginPage()
    content = canvas.drawForm(input_file, pageNo)
    template. addObject(content)
    
    # Add footer on all pages
    template.append(footer)
    
    # Add header on all pages (using myFirstPage for consistency)
    template.append(myFirstPage)
    c.BeginDocument()
    c.doForm(template)
    c.SaveState()

  c.showPage()
  c.save()

# Example usage
pdf_classification = "Confidential"
input_file = "original.pdf"
output_file = "modified.pdf"
page_size = (21, 29.7)  # Replace with your desired page size in cm (width, height)
add_header_footer(pdf_classification, input_file, output_file, page_size)

print("Successfully added header and footer to the PDF!")
