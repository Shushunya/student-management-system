import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QLabel,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

app = QApplication(sys.argv)
app_window = MainWindow()
app_window.show()
sys.exit(app.exec())
