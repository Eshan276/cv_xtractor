import os
import shutil
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.files = []

        self.status_label = QLabel("No files uploaded.")
        upload_button = QPushButton("Upload Files")
        upload_button.clicked.connect(self.upload_files)

        run_button = QPushButton("Run Custom Script")
        run_button.clicked.connect(self.run_custom_script)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(upload_button)
        layout.addWidget(run_button)  # Add the run_button to the layout

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)  # Set the layout to a widget

    def upload_files(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*)", options=options)
        if files:
            self.files.extend(files)
            self.status_label.setText(f"{len(files)} file(s) uploaded.")

    def run_custom_script(self):
        if self.files:
            self.status_label.setText("Running custom script...")
            # Add your custom script here
        else:
            self.status_label.setText("No files uploaded.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()