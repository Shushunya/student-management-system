import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog,
    QVBoxLayout, QComboBox,
    QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton
)
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        add_record_action = QAction("Add record", self)
        add_record_action.triggered.connect(self.insert_record)
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
        
    def insert_record(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add a new record")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student name")
        
        self.course = QComboBox()
        courses = ['Biology', "Math", "Astronomy", "Physics"]
        self.course.addItems(courses)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone number")

        btn = QPushButton("Register")
        btn.clicked.connect(self.add_record)

        layout.addWidget(self.student_name)
        layout.addWidget(self.course)
        layout.addWidget(self.phone)
        layout.addWidget(btn)
        self.setLayout(layout)
    
    def add_record(self):
        name = self.student_name.text()
        course = self.course.itemText(self.course.currentIndex())
        phone = self.phone.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        sql_query = "INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)"
        cursor.execute(sql_query, (name, course, phone))
        connection.commit()
        cursor.close()
        connection.close()

app = QApplication(sys.argv)
app_window = MainWindow()
app_window.show()
app_window.load_data()
sys.exit(app.exec())
