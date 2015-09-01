# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, Blueprint,  make_response, current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func
import hashlib
from unidecode import unidecode
from app import db
from app.api.v1.models import Document
import shlex
from flask.ext.restful import Api, Resource, reqparse, fields, marshal, abort
from flask.ext.httpauth import HTTPDigestAuth

mod_apiv1 = Blueprint('apiv1',__name__, url_prefix='/api/v1')
api = Api(mod_apiv1)

auth = HTTPDigestAuth()

#@auth.get_password
#def get_pw(username):
#    if username in current_app.config['API_USERS']:
#        return current_app.config['API_USERS'].get(username)
#    return None

def highlight(doc, searchs):
    content = ''
    changed = False
    contexts = []

    raw_content = doc.content
    for search in searchs:
        if search in raw_content:
            raw_content = raw_content.replace(search, '|rv|<mark>' + search + '</mark>' )
            changed = True
    if changed:
        contexts = raw_content.split('|rv|')
        content = content + '[...' + contexts[0][-70:]
        contexts.pop(0)
        for context in contexts[:-1]:
            if len(context) > 83: #70 of context and 6+7 of markup length
                content = content + context[:70] + '[..]'
            else:
                content = content + context
        content = content + contexts[-1][:70] + '...]'
        changed = False
    else:
        content = ''

    doc.content = content

    for search in searchs:
        if search in doc.name:
            doc.name = doc.name.replace(search, '<mark>' + search + '</mark>')

    return doc

class DocumentAPI(Resource):
#    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type = str, location = 'json')
        self.reqparse.add_argument('path', type = str,  location = 'json')
        self.reqparse.add_argument('content', type = str, location = 'json')
        self.reqparse.add_argument('utility', type = str, location = 'json')
        self.reqparse.add_argument('mime', type = str, location = 'json')
        self.reqparse.add_argument('pages', type = int, location = 'json')

        super(DocumentAPI, self).__init__()

    def get(self, id):
        doc = Document.query.get(id)
        if not doc: 
            abort(404, message='Document id {} not found.'.format(id))

        return {'documents': [marshal(doc, doc.marshall_fields('.document'))]}

    def put(self, id):
        doc = Document.query.get(id)    
        if not doc:
            abort(404, message='Document id {} not found.'.format(id))

        args = self.reqparse.parse_args()
     
        doc.content = unidecode(args['content'].encode('utf-8')).casefold()
        doc.name = args['name']
        doc.path = args['path']
        doc.utility = args['utility']
        doc.mime = args['mime']
        doc.pages = args['pages']
#        doc.content_hash = hashlib.sha1(args['content'].encode('utf-8')).hexdigest()
        db.session.commit()

        return { 'document' : [marshal(doc,  doc.marshall_fields('.document'))]}

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
#    decorators = [auth.login_required]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name',type = str, required = True,
             help = 'No document name provided', location = 'json')
        self.reqparse.add_argument('path',type = str, required = True,
             help = 'No document path provided', location = 'json')
        self.reqparse.add_argument('content',type = str, required = True,
             help = 'No document content provided', location = 'json')
        self.reqparse.add_argument('pages',type = str, required = True,
             help = 'No pages provided', location = 'json')
        self.reqparse.add_argument('mime',type = str, required = True,
             help = 'No mime provided', location = 'json')
        self.reqparse.add_argument('utility',type = str, required = True,
             help = 'No utility provided', location = 'json')

        super(DocumentListAPI, self).__init__()

    def get(self):

        if 'search_string' in request.args:
            normalize = unidecode(request.args.get('search_string')).casefold()
            print(normalize)
            searchs = shlex.split(normalize)
            docs = Document.query.filter(eval(build_search_condition(searchs))).all()       

            return { 'documents' : [marshal(highlight(doc, searchs),  doc.marshall_fields('.documents')) for doc in docs]}
            
        docs = Document.query.all()

        return { 'documents' : [marshal(doc,  doc.marshall_fields('.documents')) for doc in docs]}

    def put(self):
        args = self.reqparse.parse_args()
        doc = Document(args['name'],args['path'],args['mime'],args['utility'],args['pages'],args['content'])
        #doc = Document(args['name'],args['path'],args['mime'],args['utility'],args['pages'],args['content'],args['chash'] hashlib.sha1(args['content'].encode('utf-8')).hexdigest())
        db.session.add(doc)
        db.session.commit()

        return { 'document' : marshal(doc,  doc.marshall_fields('.documents'))}, 201

api.add_resource(DocumentAPI, '/documents/<int:id>', endpoint = 'document')
api.add_resource(DocumentListAPI, '/documents', endpoint = 'documents')

