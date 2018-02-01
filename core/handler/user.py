from sqlalchemy import or_
from core.models import db, User
from core.utils import create_password

class UserHandler(object):

    def __init__(self):
        pass

    def get_user(self, username):
        return User.query.filter(or_(
            User.name == username,
            User.email == username,
            User.nickname == username,
            User.real_name == username,
            User.en_name == username)).first()

    def get_list(self, keyword=None,dept_id=None,page=1, limit=30):
        query = User.query
        if keyword:
            match = '%{0}%'.format(keyword)
            query = query.filter(or_(User.name.ilike(match),
                                     User.nickname.ilike(match),
                                     User.en_name.ilike(match),
                                     User.real_name.ilike(match),
                                     User.email.ilike(match),
                                     User.wechat.ilike(match),
                                     User.phone.ilike(match)))
        if dept_id:
            query = query.filter(User.dept_id == dept_id)
        return query.paginate(page=page, per_page=limit)

    def update_passwd(self, user, password):
        user.password = create_password(password)
        db.session.add(user)
        db.session.commit()
        return user
