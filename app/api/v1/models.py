# -*- coding: utf-8 -*-
from app import db
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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    url = db.Column(db.Unicode(255))
    content = db.Column(db.UnicodeText)
    search_vector = db.Column(TSVectorType('name', 'content'))

    def __init__(self,name,url,content):
        self.name = name
        self.url = url
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)
