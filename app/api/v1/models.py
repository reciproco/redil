# -*- coding: utf-8 -*-
from app import db
import hashlib
from flask.ext.sqlalchemy import  BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType

make_searchable(options={'regconfig': 'pg_catalog.spanish'})

class DocumentQuery(BaseQuery, SearchQueryMixin):
    pass

class Document(db.Model):
    query_class = DocumentQuery
    __tablename__ = 'documents'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.Unicode(255), nullable=False)
    url            = db.Column(db.Unicode(255), nullable=False)
    content        = db.Column(db.UnicodeText, nullable=False)
    content_hash   = db.Column(db.Unicode(40), nullable=False)
    search_vector  = db.Column(TSVectorType('name', 'content'))
    __table_args__ = (db.Index('idx_documents_name_url','name','url',unique = True),) 

    def __init__(self,name,url,content, content_hash):
        self.name = name
        self.url = url
        self.content_hash = content_hash
        self.content = content

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'name'          : self.name,
            'url'           : self.url,
            'content'       : self.content,
            'content_hash'  : self.content_hash,
            'search_vector' : self.search_vector
        }
 
    def __repr__(self):
        return '<id {} name {}>'.format(self.id, self.name)
