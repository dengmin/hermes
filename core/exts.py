from datetime import datetime

from sqlalchemy import Column, DateTime
from flask_sqlalchemy import SQLAlchemy, Model

from flask_login import LoginManager


class BaseModel(Model):
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    create_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        columns = self.__table__.columns.keys()
        return {key: getattr(self, key) for key in columns}

db = SQLAlchemy(model_class=BaseModel)

login_manager = LoginManager()
login_manager.login_view = "user.login"

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))