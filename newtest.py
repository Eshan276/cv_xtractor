import os
import re
import glob
import pandas as pd
from docx import Document
import PyPDF2

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def extract_email_and_phone(text):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_regex = r'\b\d{10}\b'

    email = re.findall(email_regex, text)
    phone = re.findall(phone_regex, text)
    if(len(phone)==0):
        phone_regex = r'\b\d{5}\s\d{5}\b'
        phone = re.findall(phone_regex, text)
    return email[0] if email else None, phone[0] if phone else None

def convert_to_csv(directory):
    data = []
    for file in glob.glob(directory + "/*.pdf"):
        print(file)
        filename, file_extension = os.path.splitext(file)
        text = extract_text_pdf(file)
        email, phone = extract_email_and_phone(text)
        data.append([filename, email, phone])

    for file in glob.glob(directory + "/*.docx"):
        filename, file_extension = os.path.splitext(file)
        text = extract_text_from_docx(file)
        email, phone = extract_email_and_phone(text)
        data.append([filename, email, phone])

    df = pd.DataFrame(data, columns=['File Name', 'Email', 'Phone'])
    df.to_csv('combined.csv', index=False)
current_directory = os.getcwd()
convert_to_csv(current_directory)