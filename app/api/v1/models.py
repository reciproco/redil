# -*- coding: utf-8 -*-
from app import db
import hashlib

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

    def __init__(self,name,path,mime, utility, pages,content, chash):
        self.name = name
        self.path = path
        self.mime = mime
        self.utility = utility
        self.pages = pages
        self.chash = chash
        self.content = content

    def __repr__(self):
        return '<id {} name {}>'.format(self.id, self.name)
