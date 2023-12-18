import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QTableWidget,
    QLabel,
)
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        add_record_action = QAction("Add record", self)
        file_menu_item.addAction(add_record_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "phone"))
        self.setCentralWidget(self.table)

    def load_data(self):
        pass

app = QApplication(sys.argv)
app_window = MainWindow()
app_window.show()
sys.exit(app.exec())
