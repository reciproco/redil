# -*- coding: utf-8 -*-
from app import db
import hashlib

class Document(db.Model):
    __tablename__ = 'documents'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.Unicode(255), nullable=False)
    url            = db.Column(db.Unicode(255), nullable=False)
    content        = db.Column(db.UnicodeText, nullable=False)
    content_hash   = db.Column(db.Unicode(40), nullable=False)
    __table_args__ = (db.Index('idx_documents_name_url','name','url',unique = True),) 

    def __init__(self,name,url,content, content_hash):
        self.name = name
        self.url = url
        self.content_hash = content_hash
        self.content = content

    def __repr__(self):
        return '<id {} name {}>'.format(self.id, self.name)
