from flask import Flask, render_template, request, jsonify, Blueprint, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import db
from app.api.v1.models import Document

mod_apiv1 = Blueprint('apiv1',__name__, url_prefix='/api/v1')


@mod_apiv1.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'bad request'}),400)

@mod_apiv1.route('/documents', methods=['GET'])
def get_document():

    results = []


    rows = Document.query.all()
    for row in rows:
        results.append({'id': row.id, 'name': row.name, 'url': row.url, 'content': row.content, 'search_vector': row.search_vector})

    return jsonify({'documents': results})

@mod_apiv1.route('/search', methods=['POST'])
def search():
    if not request.json or not 'search_string' in request.json:
        raise
        abort(400)

    results = []
    q = Document.query.add_column(func.ts_headline(Document.content,func.plainto_tsquery(request.json['search_string'])))
    q = q.add_column(func.ts_headline(Document.name,func.plainto_tsquery(request.json['search_string']), 'HighlightAll=TRUE'))
    rows = q.search(request.json['search_string']).all()
    for row in rows:
        results.append({'id': row[0].id, 'name': row[0].name,
                        'url': row[0].url, 'content': row[0].content,
                        'search_vector': row[0].search_vector,
                        'ts_content': row[1],
                        'ts_name': row[2]})

    return jsonify({'results': results})
