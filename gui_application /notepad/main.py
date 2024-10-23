__author__ = 'x_spoilt'
__version__ = '1.0'



from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QTextEdit, QMessageBox, 
                             QAction, QInputDialog)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import sys
import logging, qt_material

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logs = logging.getLogger(__name__)

class Notepad(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('note.png'))
        self.__init__ui()

    def __init__ui(self):
        logs.debug('Creating UI')

        self.setWindowTitle('Notepad')
        self.setGeometry(100, 100, 800, 600)
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)
        font = QFont("Arial", 14)
        self.text_edit.setFont(font)
        self.menuBar = self.menuBar()
        file_menu = self.menuBar.addMenu('File')
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        save_as_action = QAction('Save As...', self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        new_file_action = QAction('New File', self)
        new_file_action.triggered.connect(self.new_file)
        file_menu.addAction(new_file_action)
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addAction(about_action)
        highlight_action = QAction('Highlight Text', self)
        search_action = QAction('Search Text', self)
        highlight_action.triggered.connect(self.highlight_text)
        search_action.triggered.connect(self.search_text)
        self.menuBar.addAction(highlight_action)
        self.menuBar.addAction(search_action)
    def save_file(self):
        try:
            logs.debug('Saving current file')
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(self.text_edit.toPlainText())
                QMessageBox.information(self, 'Success', 'File saved successfully')
        except Exception as e:
            logs.error(f"Error saving file: {e}")
            QMessageBox.critical(self, 'Error', f"Failed to save file: {e}")

    def search_text(self):
        try:
            logs.debug("searching text")
            search_text, ok = QInputDialog.getText(self, "Search Text", "Enter text to search:")
            if ok and search_text != '':
                cursor = self.text_edit.document().find(search_text)
                if not cursor.isNull():
                    self.text_edit.setTextCursor(cursor)
                else:
                    QMessageBox.information(self, 'Not Found', 'Text not found')
        except Exception as e:
            logs.error("Error in searching text")

    def save_file_as(self):
        try:
            logs.debug('Saving file as new file')
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)", options=options)
            if file_path:
                with open(file_path, 'w') as f:
                    f.write(self.text_edit.toPlainText())
                QMessageBox.information(self, 'Success', 'File saved successfully')
        except Exception as e:
            logs.error(f"Error in Save As: {e}")
            QMessageBox.critical(self, 'Error', f"Failed to save file: {e}")

    def new_file(self):
        logs.debug('Creating new file')
        self.text_edit.clear()

    def show_about_dialog(self):
        QMessageBox.about(self, "About Notepad", "Developed by @x_spoilt\nVersion 1.0")

    def highlight_text(self):
        logs.debug('Highlighting selected text')
        cursor = self.text_edit.textCursor()
        if cursor.hasSelection():
            text_format = cursor.charFormat()
            text_format.setBackground(QColor('yellow'))
            cursor.mergeCharFormat(text_format)
        else:
            QMessageBox.warning(self, "Highlight", "No text selected to highlight")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    qt_material.apply_stylesheet(app, theme='light_blue.xml', )

    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())
