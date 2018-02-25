import hashlib
from core.exts import db
from datetime import datetime
from flask_login.mixins import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100))
    en_name = db.Column(db.String(100), doc="英文名")
    nickname = db.Column(db.String(100), doc="花名")
    real_name = db.Column(db.String(100), doc="真实姓名")
    email = db.Column(db.String(100), doc="邮箱")
    password = db.Column(db.String(100))
    leader = db.Column(db.Integer)
    come_from = db.Column(db.String(100), doc="来自哪里")
    bianla_id = db.Column(db.INTEGER, doc="变啦ID")
    enable = db.Column(db.Boolean, default=True, doc='是否启用/禁用')
    dept_id = db.Column(db.Integer, doc="部门ID")
    post = db.Column(db.String(100), doc="职位")
    phone = db.Column(db.String(50), doc="手机号")
    wechat = db.Column(db.String(50), doc="微信号")
    score = db.Column(db.FLOAT, doc="学分")
    lastlogin = db.Column(db.DateTime, doc="上一次登录时间")

    def __init__(self, name, email):
        super().__init__()
        self.name = name
        self.email = email

    @property
    def is_active(self):
        return self.enable

    def check_passwd(self, raw):
        if '$' not in self.password:
            return False
        salt, hsh = self.password.split('$')
        passwd = '{0}{1}'.format(salt, raw)
        verify = hashlib.sha1(passwd.encode('utf-8')).hexdigest()
        return verify == hsh

    @property
    def dept(self):
        if self.dept_id:
            return Dept.query.get(self.dept_id)

    def to_dict(self):
        ret = super(User, self).to_dict()
        ret['dept'] = self.dept.name if self.dept else ''
        return ret

class Dept(db.Model):
    """"部门"""
    __tablename__ = 'dept'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100))


class Course(db.Model):
    """课程"""
    __tablename__ = 'course'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(120), doc="课程名称")
    banner = db.Column(db.String(200), doc="banner图片")
    content = db.Column(db.TEXT, doc="内容")
    remark = db.Column(db.TEXT, doc="简介摘要")
    start_time = db.Column(db.DateTime, doc="课程开始时间")
    end_time = db.Column(db.DateTime,doc="课程结束时间")
    obj = db.Column(db.String(255), doc="培训对象")
    train_type = db.Column(db.String(100), doc="培训方式")
    require = db.Column(db.String(255), doc="学员要求")
    number = db.Column(db.Integer, doc="限定人数")
    address = db.Column(db.String(200),doc="培训地址")
    category = db.Column(db.String(20), doc="课程分类")
    level = db.Column(db.String(50), doc="课程等级")
    contact = db.Column(db.String(255), doc="联系人")
    exam_type = db.Column(db.String(255), doc="考核方式")
    share = db.Column(db.TEXT, doc="课后分享")
    teachers = db.Column(db.String(255), doc="培训讲师")

class ExamResult(db.Model):
    __tablename__ = 'exam_result'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.Integer, doc="用户ID")
    course_id = db.Column(db.Integer, doc="课程ID")
    signup = db.Column(db.Boolean, doc="是否报名")
    single = db.Column(db.FLOAT, doc="单选题")
    multi = db.Column(db.FLOAT, doc="多选题")
    judge = db.Column(db.FLOAT, doc="判断题")
    answer = db.Column(db.FLOAT, doc="简答题")
    score = db.Column(db.Float, doc="总分")
    makeup = db.Column(db.FLOAT, doc="补考分数")
    sign_time = db.Column(db.DateTime, doc="报名时间")

    @property
    def average(self):
        if self.makeup == 0 or not self.makeup:
            return self.score
        return (self.score + self.makeup) / 2

    def to_dict(self):
        ret = super(ExamResult,self).to_dict()
        ret['average'] = self.average
        return ret


class ScoreHistory(db.Model):
    """学员每一次增加学分的历史记录"""
    __tablename__ = 'socre_history'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.Integer, doc="用户id")
    course_id = db.Column(db.Integer, doc="课程ID")
    score = db.Column(db.INTEGER, doc="增加的学分")
    created = db.Column(db.DateTime, doc="新增时间", default=datetime.now)


class Naire(db.Model):
    """问卷"""
    __tablename__ = 'naire'
    id = db.Column(db.INTEGER, primary_key=True)
    user_id = db.Column(db.Integer, doc="用户id")
    title = db.Column(db.String(255), doc="问卷标题")
    status = db.Column(db.Boolean, doc="发布状态")
    comment = db.Column(db.TEXT, doc="问卷介绍")
    endtime = db.Column(db.DateTime, doc="截止时间")


