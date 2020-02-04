from flask import Flask, request, render_template, jsonify
import os
import logging

from lumper import DataLumper

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/')
def main_route():
    # logger.info("Test Route")
    return'Hello World';


@app.route("/test")
def basic_template():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route('/upload', methods=['POST'])
def data_gunner():
    if not os.path.exists('Data'):
        logger.info("Creating Data Folder")
        os.mkdir('Data')
    f = request.files['file']
    f.save('Data/'+f.filename)
    logger.debug("File saved in the name {}".format(f.filename))
    # ToDO: Dataframe was creating multiple times
    x = DataLumper('Data/'+f.filename)
    column_names = x.data_frame_loader()
    # TODO: Remove this
    # cat_data, cont_data = x.data_type_explorer()
    # logger.info("Categorical columns {}".format(cat_data))
    # logger.info("Continuous columns {}".format(cont_data))
    # y = GraphAdviser(dataframe=df, continous_data=cont_data, categorical_data=cat_data)
    # charts = y.output_architect()
    names = []
    for name in column_names:
        names.append(name)
    out = {"data": {"column_names":names}}
    print(out)
    return jsonify(out)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1024)