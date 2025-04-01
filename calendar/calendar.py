from PyQt5.QtWidgets import (QMainWindow, QWidget,
                             QVBoxLayout, QCalendarWidget,
                             QPushButton, QComboBox)
import os
from main_handler.main_handler import MainHandler

directory_path = os.path.expanduser("~\\Database\\FCU")
file_names = [f for f in os.listdir(directory_path)
              if f.lower().endswith(".mdb")]


class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Date Range")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.calendar1 = QCalendarWidget()
        layout.addWidget(self.calendar1)

        self.calendar2 = QCalendarWidget()
        layout.addWidget(self.calendar2)

        self.combo_box = QComboBox()
        self.combo_box.addItems(file_names)
        layout.addWidget(self.combo_box)

        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("background-color: #008CBA; "
                                    "color: white; "
                                    "padding: 10px; "
                                    "border-radius: 5px;")
        submit_button.clicked.connect(self.on_submit)
        layout.addWidget(submit_button)

    def on_submit(self):
        start_date = self.calendar1.selectedDate().toString('yyyy/MM/dd')
        end_date = self.calendar2.selectedDate().toString('yyyy/MM/dd')
        selected_option = self.combo_box.currentText()

        handler = MainHandler(selected_option, start_date, end_date)
        handler.run()
