from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    c = canvas.Canvas("test.pdf", pagesize=letter)
    c.drawString(100, 750, "This is a test document.")
    c.drawString(100, 730, "It contains some text that we will process.")
    c.drawString(100, 710, "We will use this to test our PDF processing system.")
    c.save()

if __name__ == '__main__':
    create_test_pdf()
