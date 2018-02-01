#!/usr/bin/env python
import datetime
from flask import Blueprint, request, render_template
from core.models import db, Course, ExamResult, User
from core.handler.user import UserHandler
__all__ = ['bp']

bp = Blueprint('course', __name__)

@bp.route('/list')
def list_course():
    page = request.args.get('page', 1, int)
    limit = request.args.get('pagesize', 20, int)
    k = request.args.get('k')
    query = Course.query
    if k:
        query = query.filter(Course.name.ilike('%{0}%'.format(k)))
    try:
        depts = query.order_by(Course.id.desc()).paginate(page=page, per_page=limit)
        return {'success':True, 'data': depts.items, 'total': depts.total}
    except:
        return {'success': True, 'data':[], 'total':0}

@bp.route('/<int:course_id>')
def get_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        return {'success': True, 'data': course}
    except:
        return {'success': False, 'msg': 'not found'}

@bp.route('/create', methods=['POST'])
def create_course():
    data = request.json.copy()
    user_handler = UserHandler()
    course = Course()
    for k in data.keys():
        setattr(course, k, data.get(k))
    db.session.add(course)
    students = data.get('students')
    if students:
        students = students.split()
        for name in students:
            if name.strip():
                user = user_handler.get_user(name)
                if user:
                    er = ExamResult(user_id=user.id, course_id=course.id)
                    db.session.add(er)
                else:
                    print('user %s not found' % (name))
    db.session.commit()
    return {'success': True}

@bp.route('/edit/<int:course_id>', methods=['POST'])
def edit_course(course_id):
    try:
        user_handler = UserHandler()
        course = Course.query.get_or_404(course_id)
        data = request.json.copy()
        students = data.get('students')
        for k in data.keys():
            setattr(course, k, data.get(k))
        db.session.add(course)
        if students:
            students = students.split()
            for name in students:
                if name.strip():
                    user = user_handler.get_user(name)
                    if user:
                        er = ExamResult(user_id=user.id, course_id=course_id)
                        db.session.add(er)
                    else:
                        print('user %s not found'%(name))
        db.session.commit()
        return {'success': True, 'data':'ok'}
    except Exception as e:
        print(e)
        return {'success':False, 'msg': 'update fail!'}

@bp.route('/stds/<int:course_id>')
def student_course(course_id):
    page = request.args.get('page', 1, int)
    limit = request.args.get('pagesize', 20, int)
    results = []
    datas = db.session.query(ExamResult, User).filter(ExamResult.user_id == User.id)\
    .filter(ExamResult.course_id == course_id)
    total = datas.count()
    datas = datas.limit(limit).offset((page - 1) * limit).all()
    for exam, user in datas:
        r = exam.to_dict()
        r['username'] = user.name
        r['nickname'] = user.nickname
        results.append(r)
    return {'success': True, 'total': total, 'items': results}


@bp.route('/sign', methods=['GET'])
def to_signup():
    courses = Course.query.filter(Course.start_time >datetime.datetime.now()).order_by(Course.id.desc()).all()
    return render_template('signup.html', courses=courses)

@bp.route('/sign', methods=['POST'])
def sign_course():
    course_id = request.json.get('course_id')
    username = request.json.get('username')
    uh = UserHandler()
    user = uh.get_user(username.strip())
    if not user:
        return {'success': False, 'msg': '内网系统中没有该用户 %s'%(username)}
    exam = ExamResult.query.filter(ExamResult.course_id == int(course_id))\
        .filter(ExamResult.user_id == user.id).first()
    if exam:
        if exam.signup:
            return {'success': False, 'msg': '您已经报名了! 报名的时间是: %s'%(exam.sign_time)}
        else:
            exam.signup = True
    else:
        exam = ExamResult(course_id = int(course_id), user_id=user.id, signup=True)
    exam.sign_time = datetime.datetime.now()
    db.session.add(exam)
    db.session.commit()
    return {'success': True}


