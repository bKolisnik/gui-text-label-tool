#### Author: Cristian Mustatea
####
#### Created: July 23, 2020
#### 
import sys
import json
from os import path

class JSON_Data:
    def __init__(self,jpath='data.txt',out_path='data.txt'):
        self.out_path = out_path
        self.jpath = jpath

        if path.isfile(jpath):
            #If File exists, load it into memory
            with open(jpath) as json_file:
                self.data = json.load(json_file)
        else:
            #File not found, create new file and JSON Object
            self.data = {}
            self.data['data'] = []
            self.data['data'].append({"title":"COVID_19 Chatbot","paragraphs":[]})
       
        
    def write(self):
        with open(self.out_path, 'w') as outfile:
            json.dump(self.data, outfile)

    #Check if paragraph is already contained in JSON file
    def __pExists(self,paragraph):
        #Get list of paragraph objects
        p_list = self.data['data'][0]["paragraphs"]
        for p in p_list:
            if p["context"] == paragraph:
                return True
        return False        


    #Append a QA to the JSON
    # paragraph = paragraph string
    # question = question string
    # id = int id
    # answers = JSON Array; contains {text,answer_start}
    # is_impossible = bool 
    def append(self,paragraph,question,id,answers,is_impossible):

        a = {"text":answers[0],"answer_start":answers[1]}
        if(self.__pExists(paragraph)):
            #Check if paragraph is already contained in JSON
            q_json = {"question":question,"id":id,"answers":a,"is_impossible":is_impossible}
            for p in self.data['data'][0]["paragraphs"]:
                if p["context"] == paragraph:
                    p["qas"].append(q_json)           
        
        else:
            #If not, make a new paragraph
            temp_data = {"qas":[],"context":paragraph}
            q_json = {"question":question,"id":id,"answers":a,"is_impossible":is_impossible}
            temp_data["qas"].append(q_json)
            self.data['data'][0]["paragraphs"].append(temp_data)    

    

#Class to retrieve and update current id bookmarks
class ID_Data:
    def __init__(self,id_path="id.txt"):
        self.id_path = id_path
        self.dic = {}
        if path.isfile(id_path):
            #If File exists, load it into memory
            with open(id_path) as id_file:
                for l in id_file.readlines():
                    #Skip blank lines
                    if l in ['\n','\r\n']:
                        continue
                    temp = l.split(",")
                    self.dic[temp[0]] = int(temp[1])
        else:
            #File not found
            print("id file not found")

    def update_id(self,id):
        self.dic[id] = self.dic[id] + 1    
        #Update file
        with open(self.id_path,"w") as id_file:
            for key in self.dic:
                id_file.write(f"{key},{self.dic[key]}\n")


    #Returns id as int
    def get_id(self,id):
        return self.dic[id] 

    def get_keys(self):
        return self.dic.keys()             
                        
#Class to define the LL-like traversal through the paragraphs
class P_Data:
	def __init__(self,p_path='covid_chatbot_data.txt'):
		self.curpos = 0
		self.data = []
		self.title = []

		with open(p_path,'r') as f_open:
			for line in f_open.readlines():
				if line[0] == '#' and line[0] != '\n':
					self.title.append(line[1:])
				if line[0] != '#' and line[0] != '\n':
					self.data.append(line)
		self.len = len(self.data)
        

 	#Sets curpos to next   
	def next(self,shift=1):
		newpos = self.curpos+shift
		#If newpos is over the limit, circle to front of list
		if (newpos >(self.len-1)):
			newpos = newpos - self.len
		self.curpos = newpos
        
                       

	#Sets curpos to prev
	def prev(self,shift=1):
		newpos = self.curpos-shift
		#If newpos is under the limit, circle to end of list
		if (newpos <0):
			newpos = self.len + newpos
		self.curpos = newpos
        
	def get_curpos(self):
		return self.curpos

	def get_cur_title(self):
		return self.title[self.curpos]    

	def get_cur_paragraph(self):
		return self.data[self.curpos]
	
	def set_curpos(self,shift):
		if shift<  self.len:
			self.curpos=shift
