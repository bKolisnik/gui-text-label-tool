from os import path
import sys
#from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)

import json
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
#from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
#path.exists('../data/dataset.json')

#Class to define the LL-like traversal through the paragraphs
class P_Data:
    def __init__(self,path='covid_chatbot_data.txt'):
        self.curpos = 0
        self.data = []
        with open(path,'r') as f_open:
	        for line in f_open.readlines():
		        if line[0] != '#' and line[0] != '\n':
			        self.data.append(line)
        self.len = len(self.data)
        

    #Sets curpos to next   
    def next(self):
        newpos = self.curpos+1
        #If newpos is over the limit, circle to front of list
        if (newpos >(self.len-1)):
            newpos = newpos - self.len
        self.curpos = newpos
        
                       

    #Sets curpos to prev 
    def prev(self):
        newpos = self.curpos-1
        #If newpos is under the limit, circle to end of list
        if (newpos <0):
            newpos = self.len + newpos
        self.curpos = newpos
        

    def get_curpos(self):
        return self.curpos

    def get_cur_paragraph(self):
        print(self.data[self.curpos])
        return self.data[self.curpos]    


class Notepad(QWidget):
    def __init__(self):
        super(Notepad,self).__init__()
        #Variables to store the interval of highlighted text
        self.start = 0
        self.end = 0

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        #Set text to first Paragraph
        self.text.setText(p_data.get_cur_paragraph())
        self.text.selectionChanged.connect(self.handle_selection_changed)
        self.question = QTextEdit(self)
        #self.clr_btn = QPushButton('Clear')
        self.next_btn = QPushButton('Next')
        self.prev_btn = QPushButton('Previous')
        self.saveqa_btn = QPushButton('Save QA')
        self.saveqa_btn.setEnabled(False)
        self.text_lim = QLabel("Selection start: 0 end: 0")
        #Current Paragraph Title
        #self.p_title =  QLabel("No Paragraph Selected")
        #self.p_title.setAlignment(Qt.AlignCenter)
        #self.p_title.setTextFormat(Qt.PlainText)
        #Intialize GUI
        self.init_ui()

    #Set layout of window
    def init_ui(self):
        #titlelayout = QVBoxLayout()
        outerlayout = QVBoxLayout()
        firstlayout = QHBoxLayout()
        secondlayout = QHBoxLayout()

        #titlelayout.addWidget(self.p_title)

        firstlayout.addWidget(self.prev_btn)
        firstlayout.addWidget(self.text)
        firstlayout.addWidget(self.next_btn)
        #self.clr_btn.clicked.connect(self.clear_text)
        #add methods for other two button presses


        secondlayout.addWidget(self.question)
        secondlayout.addWidget(self.text_lim)
        secondlayout.addWidget(self.saveqa_btn)

        #outerlayout.addLayout(titlelayout)
        outerlayout.addLayout(firstlayout)
        outerlayout.addLayout(secondlayout)
        self.setLayout(outerlayout)
        self.setWindowTitle('Save QA Pairs')

        #Setting Actions for Buttons
        self.prev_btn.clicked.connect(self.prev_on_click)
        self.next_btn.clicked.connect(self.next_on_click) 

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
    
    
    def next_on_click(self):
        ##Get next paragraph and show it in text
        p_data.next()
        next_paragraph = p_data.get_cur_paragraph()
        self.text.setPlainText(next_paragraph)
        
        
    
    def prev_on_click(self):
        ##Get prev paragraph and show it in text    
        self.text.clear() 
        p_data.prev()
        next_paragraph = p_data.get_cur_paragraph()
        print(next_paragraph)
        self.text.setPlainText(next_paragraph)  

if __name__ == '__main__':
    
    p_data = P_Data()
    app = QApplication(sys.argv)
    #window = MainWindow()
    #window.show()
    writer = Notepad()
    sys.exit(app.exec_())
