# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Blueprint, abort, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
import hashlib
from app import db
from app.api.v1.models import Document

mod_apiv1 = Blueprint('apiv1',__name__, url_prefix='/api/v1')

@mod_apiv1.errorhandler(400)
def bad_request(error):
    return make_response(jsonify(error),400)

@mod_apiv1.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    results = []

    row = Document.query.get(document_id)    

    if row:
        results.append(row.serialize)
        db.session.delete(row)
        db.session.commit()
         
    return jsonify({ 'url' : request.path , 'data': results})

@mod_apiv1.route('/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):

    results = []

    row = Document.query.get(document_id)    

    if row:
        results.append(row.serialize)
         
    return jsonify({ 'url' : request.path , 'data': results})

@mod_apiv1.route('/documents', methods=['GET'])
def get_documents():

    results = []

    rows = Document.query.all()
    for row in rows:
        results.append(row.serialize)

    return jsonify({ 'url' : request.path , 'data': results})

@mod_apiv1.route('/documents', methods=['POST'])
def create_document():

    if not request.json or not 'name' in request.json or not 'url' in request.json or not 'content' in request.json:
        abort(400)
   
    results = []
 
    row = Document.query.filter(Document.url == request.json['url'],Document.name == request.json['name']).all()    

    if not row:
        d = Document(request.json['name'],request.json['url'],request.json['content'], hashlib.sha1(request.json['content'].encode('utf-8')).hexdigest())
        db.session.add(d)
        db.session.commit()
        results.append(d.serialize)

    return jsonify({'url' : request.path , 'data': results})    

@mod_apiv1.route('/documents/<int:document_id>', methods=['PUT'])
def update_document(document_id):

    results = []

    if not request.json or not 'name' in request.json or not 'url' in request.json or not 'content' in request.json:
        abort(400, {'message' : 'error in request parameters', 'data' : results })

    row = Document.query.get(document_id)    

    if row:
        results.append(row.serialize)
        row.content = request.json['content']
        row.name = request.json['name']
        row.url = request.json['url']
        row.content_hash = hashlib.sha1(request.json['content'].encode('utf-8')).hexdigest()
        db.session.commit()
        results.append(row.serialize)
         
    return jsonify({ 'url' : request.path , 'data': results})

@mod_apiv1.route('/search', methods=['POST'])
def search():

    if not request.json or not 'search_string' in request.json:
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

    return jsonify({'url' : request.path , 'data': results})
