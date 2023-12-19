import sys
import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog,
    QVBoxLayout, QComboBox, 
    QTableWidget, QTableWidgetItem,
    QLineEdit, QPushButton, QToolBar,
    QStatusBar,
)
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedHeight(400)
        self.setFixedWidth(400)

        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")
        edit_menu_item = self.menuBar().addMenu("Edit")

        add_record_action = QAction(QIcon("icons/add.png"), "Add record", self)
        add_record_action.triggered.connect(self.insert_record)
        file_menu_item.addAction(add_record_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search_dialog)
        edit_menu_item.addAction(search_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("id", "name", "course", "phone"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_record_action)
        toolbar.addAction(search_action)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        self.table.cellClicked.connect(self.cell_clicked)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        sql_query = "SELECT * FROM students"
        result = connection.execute(sql_query)
        self.table.setRowCount(0)
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
    
    def search_dialog(self):
        search = SearchDialog()
        search.exec()
    
    def cell_clicked(self):
        edit_btn = QPushButton("Edit a record")
        edit_btn.clicked.connect(self.edit)

        delete_btn = QPushButton("Delete a record")
        delete_btn.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_btn)
        self.statusbar.addWidget(delete_btn)

    def edit(self):
        dialog = Editdialog()
        dialog.exec()
    
    def delete(self):
        dialog = DeleteDialog()
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
        layout.addWidget(self.student_name)
        
        self.course = QComboBox()
        courses = ['Biology', "Math", "Astronomy", "Physics"]
        self.course.addItems(courses)
        layout.addWidget(self.course)

        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Phone number")
        layout.addWidget(self.phone)

        submit_btn = QPushButton("Submit")
        submit_btn.clicked.connect(self.add_record)
        layout.addWidget(submit_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.accept)
        layout.addWidget(cancel_btn)

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
        main_window.load_data()
        self.accept()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search a record")
        self.setFixedHeight(300)
        self.setFixedWidth(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student name")
        layout.addWidget(self.student_name)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search)
        layout.addWidget(search_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.accept)
        layout.addWidget(cancel_btn)

        self.setLayout(layout)
    
    def search(self):
        name = self.student_name.text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        sql_query = "SELECT * FROM students WHERE name = ?"
        result = cursor.execute(sql_query, (name,))

        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class Editdialog(QDialog):
    pass


class DeleteDialog(QDialog):
    pass

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
