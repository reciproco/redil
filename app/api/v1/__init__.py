# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Blueprint,  make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
import hashlib
from app import app
from app import db
from app.api.v1.models import Document
from flask.ext.restful import Api, Resource, reqparse, fields, marshal, abort

mod_apiv1 = Blueprint('apiv1',__name__, url_prefix='/api/v1')
api = Api(mod_apiv1)

document_fields = {
    'id':  fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'content': fields.String,
    'content_hash': fields.String,
    'search_vector': fields.String,
    'uri': fields.Url('.document')
}

documents_fields = {
    'id':  fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'content': fields.String,
    'content_hash': fields.String,
    'search_vector': fields.String,
    'uri': fields.Url('.documents')
}

search_fields = {
    'id':  fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'content': fields.String,
    'content_hash': fields.String,
    'search_vector': fields.String,
    'ts_name': fields.String,
    'ts_content': fields.String,
    'uri': fields.Url('.documents')
}

class DocumentAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('url', type = str,  location = 'json')
        self.reqparse.add_argument('content', type = str, location = 'json')

        super(DocumentAPI, self).__init__()

    def get(self, id):
        doc = Document.query.get(id)
        if not doc: 
            abort(404, message='Document id {} not found.'.format(id))

        return {'documents': [marshal(doc, document_fields)]}

    def put(self, id):
        doc = Document.query.get(id)    
        if not doc:
            abort(404, message='Document id {} not found.'.format(id))

        args = self.reqparse.parse_args()
     
        doc.content = args['content']
        doc.name = args['name']
        doc.url = args['url']
        doc.content_hash = hashlib.sha1(args['content'].encode('utf-8')).hexdigest()
        db.session.commit()

        return { 'document' : [marshal(doc, document_fields)]}

    def delete(self, id):
        doc = Document.query.get(id)
        if not doc: 
            abort(404, message='Document id {} not found.'.format(id))

        db.session.delete(doc)
        db.session.commit()

        return {'result': True }

class DocumentListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',type = str, required = True,
             help = 'No document name provided', location = 'json')
        self.reqparse.add_argument('url',type = str, required = True,
             help = 'No document url provided', location = 'json')
        self.reqparse.add_argument('content',type = str, required = True,
             help = 'No document content provided', location = 'json')

        super(DocumentListAPI, self).__init__()

    def get(self):

        search = request.args.get('search_string')


        if search:
            if len(search) < 4:
                return { 'documents' : []}

            search = '{}:*'.format(request.args.get('search_string'))
            query = Document.query.add_columns(func.ts_headline(Document.content,func.to_tsquery(search)).label('ts_content'))
            query = query.add_columns(func.ts_headline(Document.name,func.to_tsquery(search), 'HighlightAll=TRUE').label('ts_name'))
            docs = query.search(search).all()
       
            for doc in docs:
                doc[0].ts_content = doc[1]
                doc[0].ts_name = doc[2]
 
            return { 'documents' : [marshal(doc[0], search_fields) for doc in docs]}
            
        docs = Document.query.all()

        return { 'documents' : [marshal(doc, documents_fields) for doc in docs]}

    def put(self):
        args = self.reqparse.parse_args()
        doc = Document(args['name'],args['url'],args['content'], hashlib.sha1(args['content'].encode('utf-8')).hexdigest())
        db.session.add(doc)
        db.session.commit()

        return { 'document' : marshal(doc, documents_fields)}, 201

api.add_resource(DocumentAPI, '/documents/<int:id>', endpoint = 'document')
api.add_resource(DocumentListAPI, '/documents', endpoint = 'documents')
app.register_blueprint(mod_apiv1)

#@mod_apiv1.route('/search', methods=['POST'])
#def search():
#
#    if not request.json or not 'search_string' in request.json:
#        abort(400)
#
#    results = []
#
#    q = Document.query.add_column(func.ts_headline(Document.content,func.plainto_tsquery(request.json['search_string'])))
#    q = q.add_column(func.ts_headline(Document.name,func.plainto_tsquery(request.json['search_string']), 'HighlightAll=TRUE'))
#    rows = q.search(request.json['search_string']).all()
#    for row in rows:
#        results.append({'id': row[0].id, 'name': row[0].name,
#                        'url': row[0].url, 'content': row[0].content,
#                        'search_vector': row[0].search_vector,
#                        'ts_content': row[1],
#                        'ts_name': row[2]})
#
#    return jsonify({'url' : request.path , 'data': results})
