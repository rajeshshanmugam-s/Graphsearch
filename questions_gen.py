'''
Generate the questions based on
1. List me
2. Show me
3. segment the
4. Tell me
'''
from pprint import pprint
import yaml
import json

#fixme: write a condition in univariate question generator

q_1 = "List me the [] in data"
q_2 = "Show me the [] in data"
q_3 = "Segment the [] in data"
q_4 = "Tell me the [] in data"

def univariate_question_generator(column_names, business_column_names, id):
    if business_column_names:
        for idx, column in enumerate(column_names):
            ques = [q_1.replace('[]', column), q_2.replace('[]', column),
            q_3.replace('[]', column), q_4.replace('[]', column)]
            print(idx, column)
            ques_1 = []
            for business_column_name in business_column_names[idx]:
                 ques_1.append(q_1.replace('[]', business_column_name))
                 ques_1.append(q_2.replace('[]', business_column_name))
                 ques_1.append(q_3.replace('[]', business_column_name))
                 ques_1.append(q_4.replace('[]', business_column_name))

            out = {'type': 'intent',
                   'name': column,
                   'utterances': ques + ques_1}
            with open('Data/'+id+'.yml', 'a+') as file:
                yaml.dump(out, file, explicit_start=True)

        return "Questions Generated"


# def bivariate_questions_generator(column_names, business_column_names):
#     questions = []






# univariate_question_generator(id='6800e7b0-c1b7-4dc9-84a8-9fde957fc3a8')