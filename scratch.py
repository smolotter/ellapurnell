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
from reportlab.lib.units import mm

def add_page_numbers(input_pdf, output_pdf):
    """Adds page numbers to the top right corner of a PDF.

    Args:
        input_pdf: Path to the existing PDF file.
        output_pdf: Path to save the modified PDF file.
    """
    # Open existing PDF and create new canvas for output
    reader = canvas.open(input_pdf)
    out_canvas = canvas.Canvas(output_pdf)

    # Iterate through existing pages
    page_count = reader.getPageCount()
    for page_num in range(page_count):
        # Get page content from existing PDF
        page = reader.getPage(page_num)
        content = page.getContents()

        # Create a new page in the output PDF with the same size
        out_canvas.setPageSize(page.getPageSize())

        # Draw existing page content onto the new canvas
        out_canvas.drawContent(content)

        # Add page number text in the top right corner (adjust font size and position as needed)
        out_canvas.setFont("Helvetica", 8)  # Set font and size
        page_text = f"Page {page_num + 1} of {page_count}"
        width, height = out_canvas.pageSize  # Get page size
        out_canvas.drawRightString(width - 15*mm, height - 10*mm, page_text)  # Position text

        # Start a new page for the next iteration
        out_canvas.showPage()

    # Save the modified PDF
    out_canvas.save()

if __name__ == "__main__":
    input_pdf = "input.pdf"
    output_pdf = "output.pdf"
    add_page_numbers(input_pdf, output_pdf)
    print(f"Added page numbers to {output_pdf}")
