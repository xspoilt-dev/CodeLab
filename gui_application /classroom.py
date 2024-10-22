__author__ = "Minhajul Islam"
__email__ = "x_spoilt@yahoo.com"
__version__ = "1.0.0"
__license__ = "MIT"


import sys
import logging
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QTableWidget, 
                             QTableWidgetItem, QVBoxLayout, QWidget, QMenuBar, QMenu, QAction, 
                             QDialog, QLineEdit, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt, QEvent
import qt_material
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logs = logging.getLogger(__name__)

class ClassManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.curnt_time = datetime.now()
        self.conn = sqlite3.connect('class_data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (date TEXT, uid TEXT, name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS results (uid TEXT, subject TEXT, marks INTEGER)''')
        self.conn.commit()
        self.class_routin = {
            "Monday": [("Math", "Shawon Sir"), ("English", "Sayed Sir")],
            "Tuesday": [("Chemistry", "Sourav Sir"), ("Bangla", "Sharmin Mam")],
            "Wednesday": [("Python", "Emon Sir"), ("Electronics", "Babu Sir")],
        }
        
        self.init_ui()

    def add_attendance_to_db(self, date, uid, name):
        self.cursor.execute("INSERT INTO attendance (date, uid, name) VALUES (?, ?, ?)", (date, uid, name))
        self.conn.commit()

    def get_attendance_from_db(self, date=None):
        if date:
            self.cursor.execute("SELECT * FROM attendance WHERE date=?", (date,))
        else:
            self.cursor.execute("SELECT * FROM attendance")
        return self.cursor.fetchall()

    def add_results_to_db(self, uid, subject, marks):
        self.cursor.execute("INSERT INTO results (uid, subject, marks) VALUES (?, ?, ?)", (uid, subject, marks))
        self.conn.commit()

    def get_results_from_db(self, uid=None):
        if uid:
            self.cursor.execute("SELECT * FROM results WHERE uid=?", (uid,))
        else:
            self.cursor.execute("SELECT * FROM results")
        return self.cursor.fetchall()

    def init_ui(self):
        logs.debug("Initializing UI")
        self.setWindowTitle("Class Manager")
        self.setGeometry(100, 100, 800, 600)
        self.menubar = self.menuBar()
        self.file_menu = self.menubar.addMenu('Configure')
        self.insert_attendance_action = QAction('Insert Attendance', self)
        self.insert_attendance_action.triggered.connect(self.show_attendance_dialog)
        self.file_menu.addAction(self.insert_attendance_action)
        self.insert_results_action = QAction('Insert Results', self)
        self.insert_results_action.triggered.connect(self.show_results_dialog)
        self.file_menu.addAction(self.insert_results_action)

        layout = QVBoxLayout()
        self.attendees_button = QPushButton('Show Attendees')
        self.attendees_button.clicked.connect(self.show_attendance)
        layout.addWidget(self.attendees_button)

        self.routine_button = QPushButton('Show Class Routine')
        self.routine_button.clicked.connect(self.show_routine)
        layout.addWidget(self.routine_button)

        self.results_button = QPushButton('Show Results')
        self.results_button.clicked.connect(self.show_results)
        layout.addWidget(self.results_button)

        self.pass_button = QPushButton('Show Passed Students')
        self.pass_button.clicked.connect(self.show_passed_students)
        layout.addWidget(self.pass_button)

        self.fail_button = QPushButton('Show Failed Students')
        self.fail_button.clicked.connect(self.show_failed_students)
        layout.addWidget(self.fail_button)

        self.restrict_button = QPushButton('Show Restricted Students')
        self.restrict_button.clicked.connect(self.show_restricted_students)
        layout.addWidget(self.restrict_button)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        theme = random.choice(['dark_amber.xml',
                               'dark_blue.xml',
                               'dark_cyan.xml',
                               'dark_lightgreen.xml',
                               'dark_pink.xml',
                               'dark_purple.xml',
                               'dark_red.xml',
                               'dark_teal.xml',
                               'dark_yellow.xml'])
        qt_material.apply_stylesheet(self, theme=theme)
        self.show()

    def insert_attendance(self, dialog, date, uid, name):
        if date and uid and name:
            self.add_attendance_to_db(date, uid, name)
            QMessageBox.information(self, "Success", "Attendance added successfully!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")


    def show_results_dialog(self):
        logs.debug("Showing results dialog")
        dialog = QDialog(self)
        dialog.setWindowTitle("Insert Results")     
        form_layout = QFormLayout()
        uid_input = QLineEdit(dialog)
        subject_input = QLineEdit(dialog)
        marks_input = QLineEdit(dialog)
        form_layout.addRow("UID:", uid_input)
        form_layout.addRow("Subject:", subject_input)
        form_layout.addRow("Marks:", marks_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.insert_results(dialog, uid_input.text(), subject_input.text(), marks_input.text()))
        form_layout.addWidget(submit_button)

        dialog.setLayout(form_layout)
        dialog.exec_()
    def show_attendance_dialog(self):
        logs.debug("Showing attendance dialog")
        dialog = QDialog(self)
        dialog.setWindowTitle("Insert Attendance")  
        form_layout = QFormLayout()
        date_input = QLineEdit(dialog)
        uid_input = QLineEdit(dialog)
        name_input = QLineEdit(dialog)
        form_layout.addRow("Date (YYYY-MM-DD):", date_input)
        form_layout.addRow("UID:", uid_input)
        form_layout.addRow("Name:", name_input)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.insert_attendance(dialog, date_input.text(), uid_input.text(), name_input.text()))
        form_layout.addWidget(submit_button)
        
        dialog.setLayout(form_layout)
        dialog.exec_()
    def insert_results(self, dialog, uid, subject, marks):
        if uid and subject and marks.isdigit():
            self.add_results_to_db(uid, subject, int(marks))
            QMessageBox.information(self, "Success", "Results added successfully!")
            dialog.close()
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields with valid data")

    def add_results_to_db(self, uid, subject, marks):
        logs.debug("Adding results to database: %s, %s, %s", uid, subject, marks)
        self.cursor.execute("INSERT INTO results (uid, subject, marks) VALUES (?, ?, ?)", (uid, subject, marks))
        self.conn.commit()

    def show_attendance(self):
        logs.debug("Showing attendance")
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Date', 'UID', 'Name'])
        attendees = self.get_attendance_from_db()
        self.table.setRowCount(len(attendees))

        for i, attendee in enumerate(attendees):
            self.table.setItem(i, 0, QTableWidgetItem(attendee[0]))  # Date
            self.table.setItem(i, 1, QTableWidgetItem(attendee[1]))  # UID
            self.table.setItem(i, 2, QTableWidgetItem(attendee[2]))  # Name

    def show_routine(self):
        logs.debug("Showing class routine")
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Day', 'Subject', 'Teacher'])
        self.table.setRowCount(sum(len(routine) for routine in self.class_routin.values()))

        row = 0
        for day, routines in self.class_routin.items():
            for subject, teacher in routines:
                self.table.setItem(row, 0, QTableWidgetItem(day))
                self.table.setItem(row, 1, QTableWidgetItem(subject))
                self.table.setItem(row, 2, QTableWidgetItem(teacher))
                row += 1

    def show_results(self):
        logs.debug("Showing results")
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['UID', 'Subject', 'Marks'])
        results = self.get_results_from_db()
        self.table.setRowCount(len(results))

        for i, result in enumerate(results):
            self.table.setItem(i, 0, QTableWidgetItem(result[0]))  # UID
            self.table.setItem(i, 1, QTableWidgetItem(result[1]))  # Subject
            self.table.setItem(i, 2, QTableWidgetItem(str(result[2])))  # Marks

    def show_passed_students(self):
        logs.debug("Showing passed students")
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['UID', 'Marks'])
        passed_students = [(uid, marks) for uid, sub, marks in self.get_results_from_db() if marks >= 40]
        self.table.setRowCount(len(passed_students))

        for i, (uid, marks) in enumerate(passed_students):
            self.table.setItem(i, 0, QTableWidgetItem(uid))
            self.table.setItem(i, 1, QTableWidgetItem(str(marks)))

    def show_failed_students(self):
        logs.debug("Showing failed students")
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['UID', 'Marks'])
        failed_students = [(uid, marks) for uid, sub, marks in self.get_results_from_db() if marks < 40]
        self.table.setRowCount(len(failed_students))

        for i, (uid, marks) in enumerate(failed_students):
            self.table.setItem(i, 0, QTableWidgetItem(uid))
            self.table.setItem(i, 1, QTableWidgetItem(str(marks)))

    def show_restricted_students(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['UID', 'Status'])
        restricted_students = [(uid, "Restricted") for uid, sub, marks in self.get_results_from_db() if marks == 0]
        self.table.setRowCount(len(restricted_students))

        for i, (uid, status) in enumerate(restricted_students):
            self.table.setItem(i, 0, QTableWidgetItem(uid))
            self.table.setItem(i, 1, QTableWidgetItem(status))
    def resizeEvent(self, event):
        logs.debug("Window resized to: %s", event.size())
        super().resizeEvent(event)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized:
                logs.debug("Window maximized")
            elif self.windowState() & Qt.WindowMinimized:
                logs.debug("Window minimized")
        super().changeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassManager()
    sys.exit(app.exec_())
