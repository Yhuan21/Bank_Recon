import os
import sys
import warnings
import pyodbc
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from main_handler.main_handler import MainHandler

# Suppress the specific warning related to pandas and the database connection
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")


directory_path = os.path.expanduser("~\\Database\\FCU")  # Expands `~` to user directory
if not os.path.exists(directory_path):
    print(f"Error: The directory '{directory_path}' does not exist.")
    os.makedirs(directory_path)  # Create the directory if missing
    print(f"Created missing directory: {directory_path}")
else:
    print(f"Directory '{directory_path}' exists.")
file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
file_names = [f for f in file_names if f.lower().endswith(".mdb")]


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('basic copy.ui', self)

        # Title Bar
        self.btn_close.clicked.connect(self.closeApplication)
        self.btn_maximize_restore.clicked.connect(self.toggleMaximize)
        self.btn_minimize.clicked.connect(self.toggleMinimize)

        # Database Combo Box
        self.comboBox.addItems(file_names)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxIndexChanged)

        # Table Combo Box
        self.comboBox_2.addItems(["TRN", "TRM", "TRN_CHEQUE"])
        self.comboBox_2.currentIndexChanged.connect(self.onComboBoxIndexChanged)

        # Open Database
        self.pushButton.clicked.connect(self.on_button_click)

        # pushButton
        self.show()

    def onComboBoxIndexChanged(self, index):
        # Get the selected item from the ComboBox
        selected_item = self.comboBox.itemText(index)
        self.table = self.comboBox_2.itemText(index) if self.comboBox_2.itemText(index) else "TRN"
        self.conn = pyodbc.connect(
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + directory_path + "\\" + selected_item)
        self.TRN = pd.read_sql(sql=f"select TOP 1000 * from {self.table} ; ", con=self.conn)

        self.tableWidget.setHorizontalHeaderLabels(self.TRN.columns)
        self.tableWidget.setColumnCount(self.TRN.shape[1])
        self.tableWidget.setRowCount(self.TRN.shape[0])

        # Insert data from the DataFrame into the QTableWidget
        for row in range(self.TRN.shape[0]):
            for col in range(self.TRN.shape[1]):
                item = QTableWidgetItem(str(self.TRN.iloc[row, col]))
                self.tableWidget.setItem(row, col, item)

    def closeApplication(self):
        # Close the application when the button is clicked
        self.close()

    def toggleMaximize(self):
        if self.isMaximized():
            # If the window is maximized, restore it
            self.showNormal()
        else:
            # If the window is not maximized, maximize it
            self.showMaximized()

    def toggleMinimize(self):
        if self.isMinimized():
            # If the window is minimized, restore it
            self.showNormal()
        else:
            # If the window is not minimized, minimize it
            self.showMinimized()

    def on_button_click(self):
        self.start = self.calendarWidget.selectedDate()
        start = self.start.toString('yyyy/MM/dd')

        self.end = self.calendarWidget_2.selectedDate()
        end = self.end.toString('yyyy/MM/dd')

        selected_option = self.comboBox.currentText()
        print(selected_option)
        handler = MainHandler(selected_option, start, end)
        handler.run()

        pass

