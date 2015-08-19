from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import func

import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import Document


@app.route('/', methods=['GET', 'POST'])
def index():
#    rows = Document.query.search('pe').all()
#
#    for row in rows:
#       print(row.name + ' '+ row.url +' ' + row.content)

    q = Document.query.add_column(func.ts_headline(Document.content,func.plainto_tsquery('pez')))
    q = q.add_column(func.ts_headline(Document.name,func.plainto_tsquery('pez'), 'HighlightAll=TRUE'))
    rows = q.search('pez').all()



    for row in rows:
        print(row)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
