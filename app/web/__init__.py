# -*- coding: utf-8 -*-
from app import db
from flask import Blueprint, jsonify, make_response, render_template, safe_join, request
import io
import tempfile
from app import ocr

mod_web = Blueprint('web',__name__ ,url_prefix='/')

@mod_web.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@mod_web.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error':'method not allowed'}),405)


@mod_web.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@mod_web.route('upload', methods=['GET', 'POST'])
def upload():

    text = ''

    if request.method == 'POST':

        with tempfile.NamedTemporaryFile() as temp:
            print(dir(request.files['file0']))
            temp.write(request.files['file0'].stream.read())
            temp.flush()
            data = ocr.execute(temp.name)
            text = data['text']
            print(text)
            return make_response(jsonify({'texto': text}))
        
    return render_template('upload.html', texto = text)
