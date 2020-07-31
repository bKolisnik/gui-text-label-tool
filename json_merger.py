import json
import sys


##Helper Functions

def context_exists(json,context):
    for qas in json['data'][0]['paragraphs']:
        if qas['context']==context:
            return True
    return False

def q_obj_exists(json,q_obj,context):
    for qas in json['data'][0]['paragraphs']:
        if qas['context']==context:
            for q in qas['qas']:
                if q['question'] == q_obj['question']:
                    return True
    return False


if(len(sys.argv) < 3):
    print('Not Enough arguments')
    sys.exit()
#Import json objects    
with open(sys.argv[1]) as json_file1:
    data_1 = json.load(json_file1)
        
with open(sys.argv[2]) as json_file2:
    data_2 = json.load(json_file2)

#Create new JSON object
newj = {}
newj['data'] = []
newj['data'].append({"title":"COVID_19 Chatbot","paragraphs":[]})

#Add first file contents to new JSON
for qas in data_1['data'][0]['paragraphs']:
    newj['data'][0]['paragraphs'].append(qas)

#Iterate through all items in file 2, add questions that don't exists    
for qas_i in range(len(data_2['data'][0]['paragraphs'])):
    qas = data_2['data'][0]['paragraphs'][qas_i]
    #Check if current context has questions in file 1
    if context_exists(newj,qas['context']):
        #context exists, add the questions that don't exists
        for q_obj in qas['qas']:
            if not q_obj_exists(newj,q_obj,qas['context']):
                ##Question DNE, add it
                newj['data'][0]['paragraphs'][qas_i]['qas'].append(q_obj)
    else:
        #Context DNE, add all questions
        newj['data'][0]['paragraphs'].append(qas)


with open('merged.txt', 'w') as outfile:
    json.dump(newj, outfile)
