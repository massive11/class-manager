from . import db, app, login_manager
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from datetime import datetime


# 账户表
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.String(13), unique=True, primary_key=True, index=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    type = db.Column(db.Integer, nullable=False)  # 用户属性： 0.admin 1.student 2.instructor


# 课程表
class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.String(13), unique=True, primary_key=True, index=True)
    course_name = db.Column(db.String(32), nullable=False)
    teacher_id = db.Column(db.String(13), unique=True, primary_key=True, index=True)


# # 教师-课堂表
# class TeaCourse(db.Model):
#     __tablename__ = 'tea_courses'
#     # 教师id和课程id共同作为主键
#     course_id = db.Column(db.String(6), primary_key=True)
#     uid = db.Column(db.String(13), primary_key=True, nullable=False)


# 学生-课堂表
class StuCourse(db.Model):
    __tablename__ = 'stu_courses'
    # 学生id和课程id共同作为主键
    uid = db.Column(db.String(13), primary_key=True)
    course_id = db.Column(db.String(6), primary_key=True, nullable=False)



