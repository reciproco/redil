# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Blueprint,  make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
import hashlib
from app import db
from app.api.v1.models import Document
import shlex
from flask.ext.restful import Api, Resource, reqparse, fields, marshal, abort

mod_apiv1 = Blueprint('apiv1',__name__, url_prefix='/api/v1')
api = Api(mod_apiv1)

document_fields = {
    'id':  fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'content': fields.String,
    'content_hash': fields.String,
    'uri': fields.Url('.document')
}

documents_fields = {
    'id':  fields.Integer,
    'name': fields.String,
    'url': fields.String,
    'content': fields.String,
    'content_hash': fields.String,
    'uri': fields.Url('.documents')
}

def highlight(doc, searchs):
    content = ''
    lines = doc.content.split('\n')
    for line in lines:
        for search in searchs:
            if search in line:
                line = line.replace(search, '<b>' + search + '<\b>')
        content = content + line

    doc.content = content

    for search in searchs:
        doc.name = doc.name.replace(search, '<b>' + search + '<\b>')

    return doc

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

def build_search_condition(search):
    result = ''
    for condition in search:
        condition = condition.replace('"','')
        condition = condition.replace("'","")
        result = result + "(Document.name.like('%{}%') | Document.content.like('%{}%')) & ".format(condition,condition)

    return result[:-2]

    

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

        searchs = shlex.split(request.args.get('search_string'))

        if searchs:
            docs = Document.query.filter(eval(build_search_condition(searchs))).all()       

            return { 'documents' : [marshal(highlight(doc, searchs), documents_fields) for doc in docs]}
            
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
