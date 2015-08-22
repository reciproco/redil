# -*- coding: utf-8 -*-
from flask import Flask, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    print(os.environ['APP_SETTINGS'])
    db.init_app(app)

    from app.api.v1 import mod_apiv1
    app.register_blueprint(mod_apiv1)

    from app.web import mod_web
    app.register_blueprint(mod_web)

    app.register_error_handler(404,not_found)
    
    return app

def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
