import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
from dotenv import load_dotenv
from docx import Document
import numpy as np
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\adars\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
## Change the pytesseract file location according to your file directory

def extract_text_from_docx(file_content):
    doc = Document(io.BytesIO(file_content))
    full_text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            image_stream = io.BytesIO(rel.target_part.blob)
            image = Image.open(image_stream)
            ocr_text = pytesseract.image_to_string(image)
            full_text += ocr_text
    # full_text = remove_newlines(full_text)      
    return full_text


def extract_text_from_pdf(doc):
    full_text = ""
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        text = page.get_text("text")
        full_text += text
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            ocr_text = pytesseract.image_to_string(image)
            full_text += ocr_text
    full_text = remove_newlines(full_text)     
    return full_text

def remove_newlines(input_string):
    return input_string.replace('\n', '')

def replace_backslashes(path):
    normalized_path = os.path.normpath(path)
    return normalized_path.replace("\\", "/")

def clean_text(text):
    # Remove specific unwanted sequences
    unwanted_sequences = [
        r'\.{3,}',          # Matches sequences of three or more dots (e.g., "...")
        r'-{2,}',           # Matches sequences of two or more hyphens (e.g., "--")
        r'_{2,}',           # Matches sequences of two or more underscores (e.g., "__")
        r'\s+',             # Matches sequences of one or more whitespace characters
    ]
    for sequence in unwanted_sequences:
        text = re.sub(sequence, ' ', text)
    text = text.strip()
    return text


def process_file(contents, filename):
    contents = replace_backslashes(contents)
    if filename.endswith('.pdf'):
        doc = fitz.open(contents)
        full_text = extract_text_from_pdf(doc)
    elif filename.endswith('.docx'):
        with open(contents, "rb") as f:
            content = f.read()
        full_text = extract_text_from_docx(content)
    else:
        raise ValueError("Unsupported file format")
    full_text = clean_text(full_text)
    return full_text
# # Note name the pdf or docx file with capital first letter
# contents =  "Data\Oncology.pdf"
# filename = "Oncology.pdf"

# data = process_file(contents, filename)
# print(len(data))
