from pypdf import PdfReader, PdfWriter

reader = PdfReader("[REDACTED].pdf")
writer = PdfWriter()

for page in reader.pages:
    # Reset the viewable area to the original full size
    page.mediabox = page.artbox 
    writer.add_page(page)

with open("[REDACTED].pdf", "wb") as f:
    writer.write(f)