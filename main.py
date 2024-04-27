import sys
import os
import subprocess
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox

class FileUploader(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Uploader")
        self.setGeometry(100, 100, 400, 250)

        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.upload_button = QPushButton("Upload File(s)")
        self.upload_button.clicked.connect(self.upload_files)
        self.layout.addWidget(self.upload_button)

        self.run_script_button = QPushButton("Run Script")
        self.run_script_button.clicked.connect(self.run_newtest_script)
        self.layout.addWidget(self.run_script_button)

        self.download_csv_button = QPushButton("Download CSV")
        self.download_csv_button.clicked.connect(self.download_csv)
        self.layout.addWidget(self.download_csv_button)

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

    def run_newtest_script(self):
        script_path = os.path.join(os.path.dirname(__file__), "newtest.py")
        subprocess.Popen(["python", script_path])

    def download_csv(self):
        combined_csv_path = os.path.join(os.path.dirname(__file__), "combined.csv")
        if os.path.exists(combined_csv_path):
            save_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", os.path.expanduser("~"), "CSV Files (*.csv)")
            shutil.copy(combined_csv_path, save_path)
            QMessageBox.information(self, "Success", "Combined CSV file downloaded successfully.")

        else:
            QMessageBox.critical(self, "Error", "Combined CSV file not found.")

    def clear_cache(self):
        files_to_delete = [file for file in os.listdir() if file.endswith(('.pdf', '.docx', '.doc', '.csv'))]
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
