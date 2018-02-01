
from flask_script import Manager
from app import app, tornado_app
import tornado.httpserver
import tornado.ioloop
import tornado.netutil
import tornado.process
from core.models import *

mgr = Manager(app)

@mgr.option('-p', '--port', dest='port', default=5000)
def run(port):
    tornado_app.listen(port, xheaders=True)
    tornado.ioloop.IOLoop.current().start()

@mgr.command
def syncdb():
    db.create_all()

@mgr.command
def dropall():
    db.drop_all()

@mgr.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    mgr.run()