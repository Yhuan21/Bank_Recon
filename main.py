import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication  # Use QApplication from PyQt5.QtWidgets
from ui.ui import Ui

def date_converter(date_string: str) -> str:
    """
    Convert a date string in the format 'Wed Mar 03 2021' to 'YYYY/MM/DD'.
    """
    return datetime.strptime(date_string, "%a %b %d %Y").strftime("%Y/%m/%d")

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Use QApplication directly
    window = Ui()
    window.setWindowTitle("PyQt-Frameless-Window")
    window.show()
    sys.exit(app.exec())
