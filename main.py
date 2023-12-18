import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QTableWidget, QTableWidgetItem,
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
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        sql_query = "SELECT * FROM students"
        result = connection.execute(sql_query)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(
                    row_number, 
                    column_number, 
                    QTableWidgetItem(str(data)
                ))
        connection.close()
        

app = QApplication(sys.argv)
app_window = MainWindow()
app_window.show()
app_window.load_data()
sys.exit(app.exec())
