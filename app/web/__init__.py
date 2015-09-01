# -*- coding: utf-8 -*-
import os
from app import db
import tempfile
from flask import Blueprint, jsonify, make_response, render_template, safe_join, request, current_app
from app import ocr
from app.api.v1.models import Document
from app import q
from rq.job import Job
from worker import conn

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


@mod_web.route("results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        doc = Document.query.filter_by(id=job.result).first()
        print(doc)
        return jsonify(doc.serialize)
    else:
        return "Nay!", 202

@mod_web.route('upload', methods=['GET', 'POST'])
def upload():

    text = ''

    if request.method == 'POST':
        filename = request.files['file0'].filename

        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1], delete=False) as temp:
            temp.write(request.files['file0'].stream.read())
            temp.flush

            job = q.enqueue_call(
                func=ocr.extract_text, args=(filename,temp.name,), result_ttl=5000
            )
            print(job.get_id())
            text = job.get_id()

    return make_response(jsonify({'texto': text}))
