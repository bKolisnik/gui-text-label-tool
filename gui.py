from os import path
import sys
#from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)

import json
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
#from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
#path.exists('../data/dataset.json')



class Notepad(QWidget):
    def __init__(self):
        super(Notepad,self).__init__()
        #Variables to store the interval of highlighted text
        self.start = 0
        self.end = 0

        self.text = QTextEdit(self)
        self.text.selectionChanged.connect(self.handle_selection_changed)
        self.question = QTextEdit(self)
        #self.clr_btn = QPushButton('Clear')
        self.next_btn = QPushButton('Next')
        self.prev_btn = QPushButton('Previous')
        self.saveqa_btn = QPushButton('Save QA')
        self.saveqa_btn.setEnabled(False)
        self.text_lim = QLabel("Selection start: 0 end: 0")
        self.init_ui()

    def init_ui(self):
        outerlayout = QVBoxLayout()
        firstlayout = QHBoxLayout()
        secondlayout = QHBoxLayout()

        firstlayout.addWidget(self.prev_btn)
        firstlayout.addWidget(self.text)
        firstlayout.addWidget(self.next_btn)
        #self.clr_btn.clicked.connect(self.clear_text)
        #add methods for other two button presses


        secondlayout.addWidget(self.question)
        secondlayout.addWidget(self.text_lim)
        secondlayout.addWidget(self.saveqa_btn)

        outerlayout.addLayout(firstlayout)
        outerlayout.addLayout(secondlayout)
        self.setLayout(outerlayout)
        self.setWindowTitle('Save QA Pairs')
        self.show()

    def handle_selection_changed(self):
        cursor = self.text.textCursor()
        self.start = cursor.selectionStart()
        self.end = cursor.selectionEnd()
        if self.start == self.end:
            self.saveqa_btn.setEnabled(False)
        else:
            self.saveqa_btn.setEnabled(True)
        self.text_lim.setText(f"Selection start: {cursor.selectionStart()} end: {cursor.selectionEnd()}")

    def clear_text(self):
        self.text.clear()

    def save_text(self):
        with open('test.txt', 'w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = MainWindow()
    #window.show()
    writer = Notepad()
    sys.exit(app.exec_())
