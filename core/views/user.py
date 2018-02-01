#!/usr/bin/env python
import xlrd
from sqlalchemy import or_
from flask import Blueprint, request, render_template
from core.models import db, User, Dept
from core.handler.user import UserHandler

__all__ = ['bp']

bp = Blueprint('user', __name__)

@bp.route('/import')
def import_user():
    book = xlrd.open_workbook("/Users/dengmin/Downloads/demo.xlsx", encoding_override='utf-8')
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    for i in range(sh.nrows):
        if i in (0, 1): continue
        data = sh.row_values(i)
        user = User(name=data[0], email=data[1])
        user.real_name = data[2]
        user.en_name = data[3]
        user.nickname = data[4]
        user.post = data[5]
        user.wechat = data[7]
        user.phone = data[8]
        user.enable = False if data[10] == '封锁' else True

        dept = data[6]
        if dept:
            _dept = Dept.query.filter(Dept.name == dept.strip()).first()
            if not _dept:
                _dept = Dept(name=dept)
                db.session.add(_dept)
            user.dept_id = _dept.id
        db.session.add(user)
    db.session.commit()
    return {'success': True}

@bp.route('/list')
def list_user():
    name = request.args.get('k')
    dept_id = request.args.get('dept_id')
    page = request.args.get('page', 1, int)
    limit = request.args.get('pagesize', 20, int)
    handler = UserHandler()
    try:
        users = handler.get_list(name, dept_id, page, limit)
        return {'success':True, 'data': users.items, 'total': users.total}
    except Exception:
        return {'success':True, 'data':[], 'total':0}

@bp.route('/<int:user_id>')
def update_user(user_id):
    user = User.query.get(user_id)
    return {'success': True, 'data':user}