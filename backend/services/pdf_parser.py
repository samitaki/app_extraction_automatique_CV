import re
import pdfplumber
from io import BytesIO

def parse_pdf(file_bytes: bytes):
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        pages_text = [p.extract_text() or "" for p in pdf.pages] # full text 
        full = "\n".join(pages_text) # separe les pages par des sauts de ligne
    return full