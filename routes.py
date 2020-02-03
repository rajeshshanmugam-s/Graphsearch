from flask import Flask, request, render_template, jsonify
# import os
# import logging

app = Flask(__name__)
#
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


@app.route('/')
def main_route():
    # logger.info("Test Route")
    return'Hello World';


@app.route("/test")
def basic_template():
    return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=1024)