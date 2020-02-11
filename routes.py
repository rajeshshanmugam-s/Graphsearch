from flask import Flask, request, render_template, jsonify
import os
import logging
from uuid import uuid4

from lumper import DataLumper
from adviser import GraphAdviser
from questions_gen import univariate_question_generator
import question_recommender as qr
from nlp_engine import intents_generator
from chart_matcher import data_finder

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def main_route():
    logger.info("Test Route")
    return'Hello World'


@app.route("/test")
def basic_template():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route('/upload', methods=['POST'])
def data_gunner():
    '''
    CSV file will be received as a response. CSV file is stored under a unique id, CSV will be
    loaded as a data frame and column names of the df will be returned.
    :return: Column names in the csv file.
    '''
    if not os.path.exists('Data'):
        logger.info("Creating Data Folder")
        os.mkdir('Data')
    f = request.files['file']

    id = str(uuid4())
    f.save('Data/'+id+'.csv')
    logger.debug("File saved in the name {}".format(id))

    x = DataLumper('Data/'+id+'.csv')
    column_names, df = x.data_frame_loader()

    names = []
    for name in column_names:
        names.append(name)
    out = {
        "id": id,
        "data": {"column_names":names}
    }
    return jsonify(out)

@app.route('/trainer', methods=['POST'])
def data_trainer():
    data = request.get_json()
    logger.debug("Request for the id{}".format(data['id']))
    x = DataLumper('Data/' + data["id"]+'.csv')
    _, df = x.data_frame_loader()
    column_names = []
    cont_data = []
    cat_data = []
    business_columns = []
    cont_bus_columns = []
    cat_bus_columns = []
    for column in data['data']:
        if column['type'] == "continuous":
            cont_data.append(column['column_name'])
            cont_bus_columns.append(column['business_name'])
            business_columns.append(column['business_name'])
            column_names.append(column['column_name'])
        elif column['type'] == 'categorical':
            cat_data.append(column['column_name'])
            cat_bus_columns.append(column['business_name'])
            business_columns.append(column['business_name'])
            column_names.append(column['column_name'])

    suggesting_questions = univariate_question_generator(column_names,business_columns,data["id"])
    y = GraphAdviser(dataframe=df[:10], continous_data=cont_data, categorical_data=cat_data, id=data["id"],
                     cat_bus_columns=cat_bus_columns, cont_bus_columns=cont_bus_columns)
    charts = y.output_architect()
    if charts and suggesting_questions:
        return suggesting_questions
        # return jsonify(charts)
    else:
        return {"Status":False}

@app.route('/search', methods=['POST'])
def timely_searcher():
    data = request.get_json()
    intents = qr.suggestion_finder(data['data'], data['id'])
    return intents

@app.route('/chart_finder', methods=['POST'])
def query_matcher():
    query = request.get_json()
    question = query['data']
    id = query['id']
    input_data, intents, column_name = intents_generator(question, id)
    return jsonify(data_finder(column_name, id))





if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1024)