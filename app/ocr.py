# -*- coding: utf-8 -*-
from app.exceptions import OCRError
import errno
import subprocess
import json
import tempfile
import os
from app.api.v1.models import Document
from app import db
from app import create_app
import base64

def extract_text(filename, stream):

   myapp = create_app()

   with myapp.app_context():
     with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1]) as temp:
        raw = stream.read()
        temp.write(raw)
        temp.flush()
        data = execute(temp.name)

        doc = Document(filename,filename,data['mimetype'],data['utility'], data['pages'], base64.b64decode(data['text']).decode('utf-8')) 
        db.session.add(doc)
        db.session.commit()

        return doc.id

   return 0

def execute(input_filename):

    command = ["ocr", input_filename]

    try:
        proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except OSError as exception:
        if exception.errno == errno.ENOENT:
            raise OCRError('ocr.sh not found at ')
        else:
            raise
    else:
        return_code = proc.wait()
        if return_code != 0:
            error_text = proc.stderr.read()
            raise(OCRError(error_text))

        data = json.loads(proc.stdout.read().decode())

        return data

if __name__ == '__main__':
    import os
    here = os.path.dirname(__file__)
    data =execute('/home/sistemas/data/CompraIndra2.pdf')
    print(data['text'])
