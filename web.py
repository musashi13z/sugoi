# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_from_directory
from evaluation import detect_img

app = Flask(__name__)

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def post():
    if request.files['file'].filename != u'':
        result = detect_img(request.files['file'].read())
    else:
        result = []
    return jsonify(result=result)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
