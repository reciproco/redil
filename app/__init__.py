# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from app.api.v1 import mod_apiv1
#app.register_blueprint(mod_apiv1)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'error':'method not allowed'}),405)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
