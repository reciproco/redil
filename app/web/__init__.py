# -*- coding: utf-8 -*-
from app import db
from flask import Blueprint, jsonify, make_response, render_template, safe_join, request
import io

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

    if request.method == 'POST':

        b = io.BytesIO()

        print(request.form)
        print(dir(request.files['file1']))
        b.write(request.files['file1'].stream.read())
        b.seek(0)
        
        view = b.read(100)

        print(view[:30])

        
#        filename =  safe_join(app.config["APPLICATION_ROOT"], path)

    return render_template('upload.html')
