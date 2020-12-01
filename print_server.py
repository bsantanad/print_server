#! /usr/bin/python3
#
# author: benja santana
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# The code was heavily inspired by the flask documentation
# pylint: disable = missing-docstring
# pylint: disable = too-few-public-methods

import os
import flask
import werkzeug.utils

UPLOAD_FOLDER = '/home/pi/print_api/uploaded_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'HEIC'}

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    Check if someone is not trying to send a php file or something, 
    like that, this could harm the server
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template("index.html")

    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            return flask.render_template("oops.html")
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return flask.render_template("oops.html")
        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = UPLOAD_FOLDER + "/" + filename
            os.system(f"lp -d DeskJet_1110\
                     {filepath}") # print file
            os.system(f"rm {filepath}") # remove file
            return flask.render_template("printed.html")

        return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='8080')
