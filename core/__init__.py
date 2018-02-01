import os
import config
from datetime import datetime
from flask import Flask, request, render_template, json
from werkzeug.wrappers import Response
from core.exts import db

class CJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, bytes):
            return o.decode('utf-8')
        elif isinstance(o, db.Model):
            return o.to_dict()
        return json.JSONEncoder.default(self, o)


class JsonResult(object):
    def __init__(self, value, status=200):
        self.value = value
        self.status = status

    def to_response(self):
        return Response(json.dumps(self.value, cls=CJSONEncoder),
                        status=self.status,
                        mimetype='application/json')

class BaieException(Exception):
    def __init__(self, error, real_message=None):
        self.code, self.message, self.status = error
        if real_message is not None:
            self.message = real_message

    def to_result(self):
        return JsonResult({'msg': self.message, 'code': self.code},
                         status=self.status)

class BaieFlask(Flask):

    def make_response(self, rv):
        if isinstance(rv, dict):
            if 'code' not in rv:
                rv['code'] = 200
            rv = JsonResult(rv)
        if isinstance(rv, JsonResult):
            return rv.to_response()
        return Flask.make_response(self, rv)


def create_app():
    app = BaieFlask('baie_deploy')

    app.config.from_object(config)

    app.config.setdefault('RESTFUL_JSON',{
        'cls': CJSONEncoder
    })

    configure_logging(app)

    @app.errorhandler(BaieException)
    def baise_error_handler(err):
        return err.to_result()

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_handler(err):
        if request.is_xhr:
            if hasattr(err, 'name'):
                msg = err.name
                status = err.code
            else:
                msg = err.message
                status = 500
            return JsonResult({'message': msg, 'code': status}, status=status)
        else:
            return render_template('errors/{0}.html'.format(err.code)), err.code

    return app

def configure_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler

    log_dir = app.config.get('LOG_FOLDER')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file = os.path.join(log_dir, 'core.log')
    handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=10)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(filename)s:[line:%(lineno)d] %(message)s')
    )
    app.logger.addHandler(handler)
