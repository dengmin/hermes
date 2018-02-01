import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
SECRET_KEY = 'UavkZPScH6boxhA*&RA#hu!N'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@localhost/hermes?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
DATABASE_QUERY_TIMEOUT = 0.5
LOG_FOLDER = '/var/log/deploy'


EMAIL_SERVER = 'smtp.exmail.qq.com'
EMAIL_USER = 'dengmin@baie.com.cn'
EMAIL_PASSWORD = ''


try:
    from settings import *
except: pass