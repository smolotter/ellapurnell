from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.fonts import addFontDirectory, TTFont
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

    # Register Arial font (assuming the font file is available)
    addFontDirectory('path/to/fonts')  # Replace with actual font directory path
    arial_font = TTFont('Arial', 'arial.ttf')  # Replace with actual font file name

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
