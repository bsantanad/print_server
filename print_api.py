#! /usr/bin/python3
#
# author: benja santana
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET': 
        return flask.render_template("index.html")

    if flask.request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in flask.request.files:
            flask.flash('No file part')
            return flask.redirect(request.url)
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flask.flash('No selected file')
            return flask.redirect(request.url)
        if file and allowed_file(file.filename):
            filename = werkzeug.utils.secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #os.system('lp -d HPLaserJ {0}')
            return "done"
        
        return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8080')
