from request import RequestManager
import random
import json

request_manager =  RequestManager()


def get_more_questions(type,n_questions=10):
    list_questions=[]
    list_options=[]
    list_answers=[]
    i=1

    if type=='conflicts':

        while i<=n_questions:
            element, to_ask, answer, options = request_manager.generate_conflict_question()
            if len(options)==3 and 'itemLabel' not in to_ask:

                if 'location' in to_ask:
                    to_ask='Where did the following event : ' + element + ' happened?'
                elif 'participantLabel' in to_ask:
                    to_ask='Who participated in the following event : ' + element + ' ?'
                elif 'endDate' in to_ask:
                    to_ask='When did the following event : ' + element +' ended?'

                    answer=answer.split('-')[0]
                    options=[i.split('-')[0] for i in options]

                elif 'countryLabel' in to_ask:
                    to_ask='In which country the following event : ' + element+' happened?'
                elif 'startDate' in to_ask:
                    to_ask='When did the following event : '+ element + ' started?'
                    answer=answer.split('-')[0]
                    options=[i.split('-')[0] for i in options]
                list_questions.append(to_ask)
                idx=random.randrange(0, len(options)+1)
                options.insert(idx,answer)
                list_options.append(options)
                list_answers.append(idx+1)
                i+=1
    if type=='cities':
        already_listed=[]
        while i<=n_questions:
            element, to_ask, answer, options = request_manager.generate_city_question()
            if len(options)==3 and to_ask not in already_listed:
                already_listed.append(to_ask)
                to_ask='In which country is the city of '+to_ask+' located?'
                list_questions.append(to_ask)
                idx=random.randrange(0, len(options)+1)
                options.insert(idx,answer)
                list_options.append(options)
                list_answers.append(idx+1)
                i+=1
    return list_questions,list_answers,list_options


list_questions,list_answers,list_options=get_more_questions('cities',10)

data = {"question":list_questions, "answer":list_answers,"options":list_options}
jsonString = json.dumps(data)
jsonFile = open("data_quizz.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
