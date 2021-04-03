from . import db, app, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime


# 账户表
class Account(UserMixin, AnonymousUserMixin, db.Model):
    __tablename__ = 'accounts'
    account = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True)
    password = db.Column(db.String(32), nullable=False)
    type = db.Column(db.String(16), nullable=False)

    def show(self):
        return [self.account, self.password, self.type]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.account


class AnonymousUser(AnonymousUserMixin):
    def can(self):
        return False

    def is_admin(self):
        return False


# 学生表
class Student(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'students'
    id = db.Column(
        db.String(32),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True)
    name = db.Column(db.String(32), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def show(self):
        return [self.id, self.name, self.year]


# 教师表
class Instructor(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'instructors'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(32), nullable=False)

    def show(self):
        return [self.id, self.name]


# 管理员表
class Admin(db.Model, UserMixin, AnonymousUserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.String(32), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(32), nullable=False)

    def show(self):
        return [self.id, self.name]


# 课程表
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.String(13), unique=True, primary_key=True, index=True)
    course_name = db.Column(db.String(32), nullable=False)
    teacher_id = db.Column(db.String(13), unique=True, primary_key=True, index=True)


# 学生-课堂表
class StuCourse(db.Model):
    __tablename__ = 'stu_courses'
    # 学生id和课程id共同作为主键
    uid = db.Column(db.String(13), primary_key=True)
    course_id = db.Column(db.String(6), primary_key=True, nullable=False)



