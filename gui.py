from os import path
import sys
#from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)

import json
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout,QComboBox,QDialog
from PyQt5.QtCore import Qt
#from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
#path.exists('../data/dataset.json')

from gui_utils import P_Data,JSON_Data,ID_Data


class shiftPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)
        self.init_ui()
        self.shift = 0
        

    def init_ui(self):
        self.text_to_jump = QTextEdit()
        self.text_to_jump.setFocus()
        self.text_to_jump.selectionChanged.connect(self.handle_selection_changed)
        self.jump_btn = QPushButton("Go")
        self.jump_btn.clicked.connect(self.go_on_click)
        self.jump_btn.setEnabled(False)
        self.outerlayout = QVBoxLayout()
        self.outerlayout.addWidget(self.text_to_jump)
        self.outerlayout.addWidget(self.jump_btn)
        self.setLayout(self.outerlayout)
        self.setWindowTitle('Jump to Paragraph')

    def handle_selection_changed(self):
        try:
            int(self.text_to_jump.toPlainText())
            self.jump_btn.setEnabled(True)
        except:
            self.jump_btn.setEnabled(False)

    def go_on_click(self):
        self.shift = int(self.text_to_jump.toPlainText())
        self.close()

    def get_shift(self):
        return self.shift
             
           

class Notepad(QWidget):
    def __init__(self):
        super(Notepad,self).__init__()

        #Setup id user list   
        self.id_cb = QComboBox()
        self.id_cb.addItems(id_data.get_keys())
        self.id_cb.currentIndexChanged.connect(self.id_cb_selection_changed)

        #self.id stores current user id
        self.id = self.id_cb.itemText(0)

        #isImpossible Flag
        self.isImpossible_title = QLabel("isImpossible")
        self.isImpossible_cb = QComboBox()
        self.isImpossible_cb.addItems(["False","True"])
        self.isImpossible_cb.currentIndexChanged.connect(self.isImpossible_cb_selection_changed)
        self.isImpossible = False
        
        
        #Variables to store the interval of highlighted text
        self.start = 0
        self.end = 0
        self.highlighted = ""

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        #Set text to first Paragraph
        self.text.setText(p_data.get_cur_paragraph())
        self.text.selectionChanged.connect(self.handle_selection_changed)
        self.question = QTextEdit(self)

        #Current Paragraph Title
        self.p_title =  QLabel(p_data.get_cur_title()+str(p_data.get_curpos()))
        self.p_title.setAlignment(Qt.AlignCenter)
        self.p_title.setTextFormat(Qt.PlainText)

        #Text to jump to paragraph
        self.popUp = shiftPopup()
        self.p_jump_btn = QPushButton('Jump to')
        self.p_jump_btn.clicked.connect(self.jump_to_on_click)
        
        
        #self.clr_btn = QPushButton('Clear')
        self.next_btn = QPushButton('Next')
        self.next_btn.clicked.connect(self.next_on_click) 
        self.prev_btn = QPushButton('Previous')
        self.prev_btn.clicked.connect(self.prev_on_click)
        self.saveqa_btn = QPushButton('Save QA')
        self.saveqa_btn.setEnabled(False)
        self.saveqa_btn.clicked.connect(self.save_qa_on_click)
        self.text_lim = QLabel("Selection start: 0 end: 0")
        
        #Intialize GUI
        self.init_ui()

    #Set layout of window
    def init_ui(self):
        titlelayout = QVBoxLayout()
        outerlayout = QVBoxLayout()
        firstlayout = QHBoxLayout()
        firstlayout_v = QVBoxLayout()
        secondlayout = QHBoxLayout()
        secondlayout_h_layout = QVBoxLayout()


        titlelayout.addWidget(self.p_title)

        firstlayout.addWidget(self.prev_btn)
        firstlayout.addWidget(self.text)
        firstlayout.addWidget(self.next_btn)
        firstlayout_v.addWidget(self.id_cb,0,Qt.AlignBottom)
        firstlayout_v.addWidget(self.p_jump_btn,0,Qt.AlignTop)
        firstlayout.addLayout(firstlayout_v)
        #self.clr_btn.clicked.connect(self.clear_text)
        #add methods for other two button presses

        secondlayout_h_layout.addWidget(self.saveqa_btn)
        secondlayout_h_layout.addWidget(self.isImpossible_title,0,Qt.AlignBottom)
        secondlayout_h_layout.addWidget(self.isImpossible_cb,0,Qt.AlignTop)
        secondlayout.addWidget(self.question)
        secondlayout.addWidget(self.text_lim)
        secondlayout.addLayout(secondlayout_h_layout)

        outerlayout.addLayout(titlelayout)
        outerlayout.addLayout(firstlayout)
        outerlayout.addLayout(secondlayout)
        self.setLayout(outerlayout)
        self.setWindowTitle('Save QA Pairs')

       

        self.show()

    def id_cb_selection_changed(self,i):
        self.id = self.id_cb.itemText(i)

    def isImpossible_cb_selection_changed(self,i):
        self.isImpossible = self.isImpossible_cb.itemText(i)
        print(self.isImpossible)    

    def handle_selection_changed(self):
        cursor = self.text.textCursor()
        self.start = cursor.selectionStart()
        self.end = cursor.selectionEnd()
        if self.start == self.end:
            self.saveqa_btn.setEnabled(False)
        else:
            self.saveqa_btn.setEnabled(True)
        self.text_lim.setText(f"Selection start: {cursor.selectionStart()} end: {cursor.selectionEnd()}")
        self.highlighted = p_data.get_cur_paragraph()[cursor.selectionStart():cursor.selectionEnd()]


    def clear_text(self):
        self.text.clear()

    def save_text(self):
        with open('test.txt', 'w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)


    def save_qa_on_click(self):
        question = self.question.toPlainText()
        json_data.append(paragraph=p_data.get_cur_paragraph(),question=question,id=id_data.get_id(self.id),answers=[self.highlighted,self.start],is_impossible=self.isImpossible)
        json_data.write()
        id_data.update_id(self.id)

    ##Get next paragraph and show it in text
    def next_on_click(self):
        p_data.next()
        next_paragraph = p_data.get_cur_paragraph()
        self.text.setPlainText(next_paragraph)
        self.p_title.setText(p_data.get_cur_title()+str(p_data.get_curpos()))
        
        
    ##Get prev paragraph and show it in text 
    def prev_on_click(self):
        p_data.prev()
        next_paragraph = p_data.get_cur_paragraph()
        self.text.setPlainText(next_paragraph)
        self.p_title.setText(p_data.get_cur_title()+str(p_data.get_curpos()))

    #Jump to another paragraph
    def jump_to_on_click(self):
        #Pop up a window
        self.popUp.exec_()
        p_data.set_curpos(self.popUp.get_shift())
        next_paragraph = p_data.get_cur_paragraph()
        self.text.setPlainText(next_paragraph)
        self.p_title.setText(p_data.get_cur_title()+str(p_data.get_curpos()))


if __name__ == '__main__':
    #SETUP Helper objects
    id_data = ID_Data()
    json_data = JSON_Data()
    p_data = P_Data()

    app = QApplication(sys.argv)
    #window = MainWindow()
    #window.show()
    writer = Notepad()
    sys.exit(app.exec_())
