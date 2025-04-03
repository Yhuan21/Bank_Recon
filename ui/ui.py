import os
import sys
import warnings
import pyodbc
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from helpers.helpers import Helpers
from main_handler.main_handler import MainHandler
import json

# Suppress the specific warning related to pandas and the database connection
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

with open('config.json') as f:
    config = json.load(f)

directory_path = os.path.expanduser(config["directory_path"])
default_directory_path = os.path.expanduser(config["default_directory_path"])

file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
file_names = [f for f in file_names if f.lower().endswith(".mdb")]


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        uic.loadUi("basic.ui", self)
        self.helper = Helpers()
        self.setup_vars()
        self.show()

    def setup_vars(self):
        """Set up UI variable connections."""
        self.btn_close.clicked.connect(self.closeApplication)
        self.btn_maximize_restore.clicked.connect(self.toggleMaximize)
        self.btn_minimize.clicked.connect(self.toggleMinimize)

        self.drive_combo_box.addItems(self.helper.drive_letters)
        self.drive_box_change(0)
        self.drive_combo_box.currentIndexChanged.connect(self.drive_box_change)
        self.create_csv_button.clicked.connect(self.create_csv)

    def drive_box_change(self, index: int):
        """Update the company box based on the selected drive."""
        drive_letter = (
            self.drive_combo_box.itemText(index) or self.drive_combo_box.currentText()
        )
        companies = self.helper.get_company_folders(drive_letter)
        self.company_box.clear()
        (
            self.company_box.addItems(companies)
            if companies
            else self.status_box.setText("STATUS: No Company Folder Found")
        )
        self.status_box.setText(
            f"STATUS: {len(companies)} company found"
            if companies
            else "STATUS: No Company Folder Found"
        )

    def closeApplication(self):
        """Close the application."""
        self.close()

    def toggleMaximize(self):
        """Toggle between maximizing and restoring the window."""
        self.showNormal() if self.isMaximized() else self.showMaximized()

    def toggleMinimize(self):
        """Minimize the window."""
        self.showNormal() if self.isMinimized() else self.showMinimized()

    def create_csv(self):
        """Create a CSV file based on selected date range and company."""
        start = self.start_date_widget.selectedDate().toString("yyyy/MM/dd")
        end = self.end_date_widget.selectedDate().toString("yyyy/MM/dd")

        self.progressBar.setVisible(True)
        self.progressBar.setValue(10)
        company = self.company_box.currentText()
        directory_path = os.path.join(
            self.drive_combo_box.currentText(), "bank_recon", company
        )

        handler = MainHandler(start, end, company, directory_path)
        handler.run()
        self.progressBar.setValue(100)


