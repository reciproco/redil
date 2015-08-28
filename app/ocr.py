# -*- coding: utf-8 -*-
from app.exceptions import OCRError
import errno
import subprocess
import json

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
