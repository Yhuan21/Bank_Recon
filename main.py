import sys
from PyQt5.QtWidgets import QApplication
from ui.ui import Ui


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    window.setWindowTitle("Bank Recon")
    window.show()
    sys.exit(app.exec())
