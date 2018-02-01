from flask import render_template
from core import create_app

from core.exts import db, login_manager
from flask_restful import Api

from tornado.web import Application as TornadoApp, FallbackHandler
from tornado.wsgi import WSGIContainer


app = create_app()
db.init_app(app)
api = Api(app)
login_manager.init_app(app)

from core.views import user, dept, course
app.register_blueprint(user.bp, url_prefix='/user')
app.register_blueprint(dept.bp, url_prefix='/dept')
app.register_blueprint(course.bp, url_prefix='/course')

tornado_container = WSGIContainer(app)

tornado_app = TornadoApp([
    (r'.*', FallbackHandler, dict(fallback=tornado_container))
], debug=True)


@app.teardown_request
def req_tera_down(response):
    db.session.remove()

@app.route('/')
def index():
    return render_template('index.html')
