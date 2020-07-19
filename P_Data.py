#### Author: Cristian Mustatea
#### 

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