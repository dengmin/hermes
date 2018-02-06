#!/usr/bin/env python
import datetime
import uuid
import os
import xlrd
from sqlalchemy import or_
from flask import Blueprint, request, render_template
from core.models import db, Course, ExamResult, User, Dept
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
                        exam = ExamResult.query.filter(ExamResult.user_id == user.id)\
                            .filter(ExamResult.course_id == course_id).first()
                        if not exam:
                            exam = ExamResult(user_id=user.id, course_id=course_id)
                        else:
                            print('exam exists')
                        db.session.add(exam)
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
    dept_id = request.args.get('dept_id')
    username = request.args.get('username')
    results = []
    datas = db.session.query(ExamResult, User).filter(ExamResult.user_id == User.id)\
    .filter(ExamResult.course_id == course_id)
    if dept_id:
        datas = datas.filter(User.dept_id == int(dept_id))
    if username:
        datas = datas.filter(or_(
            User.nickname.ilike('%{}%'.format(username)),
            User.real_name.ilike('%{}%'.format(username)),
            User.en_name.ilike('%{}%'.format(username)),
        ))
    datas = datas.order_by(ExamResult.score)
    total = datas.count()
    datas = datas.limit(limit).offset((page - 1) * limit).all()
    for exam, user in datas:
        r = exam.to_dict()
        r['username'] = user.real_name
        r['nickname'] = user.nickname
        r['dept'] = user.dept.name if user.dept else ''
        r['post'] = user.post
        results.append(r)
    return {'success': True, 'total': total, 'items': results}

@bp.route('/score/<int:course_id>', methods=['POST'])
def socre_course(course_id):
    user_id = request.json.get('user_id')
    exam = ExamResult.query.filter(ExamResult.user_id==int(user_id)).filter(ExamResult.course_id == course_id).first()
    if not exam:
        exam = ExamResult(course_id=course_id, user_id=user_id)
    exam.single = int(request.json.get('single'))
    exam.multi = int(request.json.get('multi'))
    exam.judge = int(request.json.get('judge'))
    exam.answer = int(request.json.get('answer'))
    exam.makeup = int(request.json.get('makeup'))
    exam.score = (exam.single + exam.multi + exam.judge + exam.answer)
    db.session.add(exam)
    db.session.commit()
    return {'success':True, 'data': exam}

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ('xls', 'xlsx')

@bp.route('/import/<int:course_id>', methods=['POST'])
def import_score(course_id):
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4())
        path = os.path.join('/tmp', filename)
        file.save(path)
        # 从Excel中读取文件
        book = xlrd.open_workbook(path, encoding_override='utf-8')
        sh = book.sheet_by_index(0)
        for i in range(sh.nrows):
            if i <=3: continue
            row = sh.row_values(i)
            dept_name = row[1]

            #设置部门
            dept = Dept.query.filter(Dept.name == dept_name).first()
            if not dept:
                dept = Dept(name=dept_name)
                db.session.add(dept)
            realname = row[3].strip()
            nickname = row[4].strip()
            #设置用户
            user = None
            if realname:
                user = User.query.filter(User.real_name == realname).first()
            else:
                if nickname:
                    user = User.query.filter(User.nickname == nickname).first()
            if not user:
                name = nickname if nickname else realname
                user = User(name=name, email=None)
            user.nickname = nickname
            user.real_name = realname
            user.dept_id = dept.id
            user.post = row[2]
            db.session.add(user)

            #设置分数
            exam = ExamResult.query.filter(ExamResult.course_id==course_id)\
                .filter(ExamResult.user_id == user.id).first()
            if not exam:
                exam = ExamResult(course_id=course_id, user_id=user.id)
            exam.single = row[5]
            exam.multi = row[6]
            exam.judge = row[7]
            exam.answer = row[8]
            exam.score = row[9]
            if row[10]:
                exam.makeup = row[10]
            db.session.add(exam)
            db.session.commit()
        os.remove(path)
    else:
        return {'success': False, 'msg': '文件格式不对'}
    return {}


