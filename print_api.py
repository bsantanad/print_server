#! /usr/bin/python3
#
# author: benja santana
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# pylint: disable = missing-docstring 
# pylint: disable = too-few-public-methods 
import flask
import flask_restful

app = flask.Flask(__name__)
api = flask_restful.Api(app)

class Printy(flask_restful.Resource):
    """
    This class manage the request for printing things

    post -> recive a document and print it
    """
    def post(self):
        return 0;


@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')
