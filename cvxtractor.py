import os
import re
import sys
import glob
import shutil
from docx import Document
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox
import xlwt

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
    if len(phone) == 0:
        phone_regex = r'\b\d{5}\s\d{5}\b'
        phone = re.findall(phone_regex, text)
    return email[0] if email else None, phone[0] if phone else None

def convert_to_xls(directory):
    data = []
    for file in glob.glob(directory + "/*.pdf"):
        filename, file_extension = os.path.splitext(file)
        text = extract_text_pdf(file)
        email, phone = extract_email_and_phone(text)
        remaining_text = text
        if email:
            remaining_text = remaining_text.replace(email, '')
        if phone:
            remaining_text = remaining_text.replace(phone, '')
        data.append([filename, email, phone, remaining_text])

    for file in glob.glob(directory + "/*.docx"):
        filename, file_extension = os.path.splitext(file)
        text = extract_text_from_docx(file)
        email, phone = extract_email_and_phone(text)
        remaining_text = text
        if email:
            remaining_text = remaining_text.replace(email, '')
        if phone:
            remaining_text = remaining_text.replace(phone, '')
        data.append([filename, email, phone, remaining_text])

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')
    for i, row in enumerate(data):
        for j, value in enumerate(row):
            ws.write(i, j, value)
    wb.save('combined.xls')


class FileUploader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CV_Xtractor")
        self.setGeometry(100, 100, 400, 250)

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.upload_button = QPushButton("Upload File(s)")
        self.upload_button.clicked.connect(self.upload_files)
        self.layout.addWidget(self.upload_button)

        self.run_script_button = QPushButton("Run Script")
        self.run_script_button.clicked.connect(self.run_script)
        self.layout.addWidget(self.run_script_button)

        self.download_xls_button = QPushButton("Download XLS")
        self.download_xls_button.clicked.connect(self.download_xls)
        self.layout.addWidget(self.download_xls_button)

        self.clear_cache_button = QPushButton("Clear Cache")
        self.clear_cache_button.clicked.connect(self.clear_cache)
        self.layout.addWidget(self.clear_cache_button)

    def upload_files(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Documents (*.docx *.doc *.pdf)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            for file_path in selected_files:
                file_name = os.path.basename(file_path)
                file_extension = os.path.splitext(file_name)[1]
                if file_extension.lower() in ['.docx', '.doc', '.pdf']:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    with open(file_name, 'wb') as f:
                        f.write(content)
                    print(f"File '{file_name}' saved in the same directory as the script.")
                else:
                    print(f"File '{file_name}' is not supported.")
            self.run_script_button.setEnabled(True)  # Enable the button after files uploaded

    def run_script(self):
        current_directory = os.getcwd()
        convert_to_xls(current_directory)

    def download_xls(self):
        current_directory = os.getcwd()
        combined_xls_path = os.path.join(current_directory, "combined.xls")
        if os.path.exists(combined_xls_path):
            save_path, _ = QFileDialog.getSaveFileName(self, "Save XLS File", os.path.expanduser("~"), "Excel Files (*.xls)")
            if save_path:  # Check if a file name was entered in the Save dialog
                shutil.copy(combined_xls_path, save_path)
                QMessageBox.information(self, "Success", "Combined XLS file downloaded successfully.")
        else:
            QMessageBox.critical(self, "Error", "Combined XLS file not found.")

    def clear_cache(self):
        files_to_delete = [file for file in os.listdir() if file.endswith(('.pdf', '.docx', '.doc', '.xls'))]
        if files_to_delete:
            for file in files_to_delete:
                os.remove(file)
            QMessageBox.information(self, "Success", "Cache cleared successfully.")
        else:
            QMessageBox.warning(self, "Warning", "No cache files found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileUploader()
    window.show()
    sys.exit(app.exec_())
