from flask import current_app, Markup, render_template, request, jsonify, make_response
from werkzeug.exceptions import default_exceptions, HTTPException


def error_handler(error):
    msg = "Request resulted in {}".format(error)
    current_app.logger.warning(msg, exc_info=error)

    if isinstance(error, HTTPException):
        description = error.get_description(request.environ)
        code = error.code
        name = error.name
    else:
        description = ("We encountered an error "
                       "while trying to fulfill your request")
        code = 500
        name = 'Internal Server Error'

    return make_response(jsonify({'error' : code, 'name' : name, 'message': description}))

def init_errors(app):
    for exception in default_exceptions:
        app.register_error_handler(exception, error_handler)

    app.register_error_handler(Exception, error_handler)

