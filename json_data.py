import json
from os import path

class Json_Data:
    def __init__(self,jpath='json.txt',out_path='data.txt'):
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
        
        if(self.__pExists(paragraph)):
            #Check if paragraph is already contained in JSON
            q_json = {"question":question,"id":id,"answers":answers,"is_impossible":is_impossible}
            for p in self.data['data'][0]["paragraphs"]:
                if p["context"] == paragraph:
                    p["qas"].append(q_json)
        
        else:
            #If not, make a new paragraph
            temp_data = {"qas":[],"context":paragraph}
            q_json = {"question":question,"id":id,"answers":answers,"is_impossible":is_impossible}
            temp_data["qas"].append(q_json)
            self.data['data'][0]["paragraphs"].append(temp_data)    

       

# For testing
#if __name__ == '__main__':
#    j = Json_Data("json_2.txt")
#    j.append("TEST","Who is BEyonce",2222,[{"text":"she is queen","answer_start":207}],False)
#    j.append("TEST","When did xxy",555,[{"text":"in the 90s","answer_start":269}],False)
#    j.write()