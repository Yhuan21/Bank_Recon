import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from ui.ui import Ui

# Print the list of file names
def date_converter(date_string: str):
    import datetime
    # Sample date string
    # Parse the date string into a datetime object
    date_object = datetime.datetime.strptime(date_string, "%a %b %d %Y")
    datetime64_object = date_object.strftime('%Y/%m/%d')
    # Extract month, day, and year from the datetime object
    return datetime64_object


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = CalendarApp()
    # window.show()

    window = Ui()
    window.setWindowFlags(window.windowFlags() | Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())
