# -*- coding: utf-8 -*-
from app import db
import hashlib
from unidecode import unidecode
from flask.ext.restful import fields

class Document(db.Model):
    __tablename__ = 'documents'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.Unicode(255), nullable=False)
    path           = db.Column(db.Unicode(255), nullable=False)
    mime           = db.Column(db.Unicode(32), nullable=False)
    utility        = db.Column(db.Unicode(32), nullable=False)
    pages          = db.Column(db.Integer, nullable=False)
    content        = db.Column(db.UnicodeText, nullable=False)
    chash          = db.Column(db.Unicode(40), nullable=False)
    __table_args__ = (db.Index('idx_documents_chash','chash',unique = True),) 

    def __init__(self,name,path,mime, utility, pages,content):
        self.name = name
        self.path = path
        self.mime = mime
        self.utility = utility
        self.pages = pages
        self.chash = hashlib.sha1(content.encode('utf-8')).hexdigest()
        self.content = unidecode(content).casefold()

    @property
    def serialize(self):
        return {
            'id' : self.id,
            'path': self.path,
            'mime': self.mime,
            'utility': self.utility,
            'pages': self.pages,
            'content': self.content,
            'chash': self.chash
        }

    def marshall_fields(self, endpoint):
        return {
            'id':     fields.Integer,
            'name':   fields.String,
            'path':   fields.String,
            'pages':  fields.Integer,
            'mime':   fields.String,
            'utility': fields.String,
            'content': fields.String,
            'chash': fields.String,
            'uri': fields.Url(endpoint)
        }

    def __repr__(self):
        return '<id {} name {}>'.format(self.id, self.name)
