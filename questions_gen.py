'''
Generate the questions based on
1. List me
2. Show me
3. segment the
4. Tell me
'''
import yaml
import logging
import random


logger = logging.getLogger(__name__)

#fixme: write a condition in univariate question generator

q_1 = "List me the [] in data"
q_2 = "Show me the [] in data"
q_3 = "Segment the [] in data"
q_4 = "Tell me the [] in data"

#Fixme: Send the chart data for resposne

def univariate_question_generator(column_names, business_column_names, id):
    suggesting_questions = []
    if business_column_names:
        for idx, column in enumerate(column_names):
            ques = [q_1.replace('[]', column), q_2.replace('[]', column),
            q_3.replace('[]', column), q_4.replace('[]', column)]
            logger.debug("Generating univariate questions for {}".format(column))
            ques_1 = []
            for business_column_name in business_column_names[idx]:
                 ques_1.append(q_1.replace('[]', business_column_name))
                 ques_1.append(q_2.replace('[]', business_column_name))
                 ques_1.append(q_3.replace('[]', business_column_name))
                 ques_1.append(q_4.replace('[]', business_column_name))
            suggesting_questions.append(ques_1[random.choice([0,1,2,3])])

            out = {'type': 'intent',
                   'name': column,
                   'utterances': ques + ques_1}
            with open('Data/'+id+'.yml', 'a+') as file:
                yaml.dump(out, file, explicit_start=True)

        logger.info('Questions generated')
        return {"questions":suggesting_questions}


# def bivariate_questions_generator(column_names, business_column_names):
#     questions = []