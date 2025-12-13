import re
import pdfplumber

def parse_pdf(path):
    with pdfplumber.open(path) as pdf:
        pages_text = [p.extract_text() or "" for p in pdf.pages] # full text 
        full = "\n".join(pages_text) # separe les pages par des sauts de ligne
    return full