from . import student
from .. import db, login_manager
from ..models import *
from flask import request, jsonify
from flask_login import current_user, login_required, login_manager
from datetime import datetime
login_manager.login_view = 'main.no_login'


# 展示学生加入的课堂
@student.route('/mine_class', methods=['GET'])
@login_required
def mine_class():
    result = []
    my_classes = StuCourse.query.filter_by(uid=current_user.id).all()
    if len(my_classes) > 0:
        schs = Course.query.filter(Course.course_id.in_([c.course_id for c in my_classes])).all()
        for sch in schs:
            tea = Instructor.query.filter_by(id=sch.teacher_id).first()
            re = {'course_id': sch.course_id,
                  'course_name': sch.course_name,
                  'instructor_name': tea.name}
            result.append(re)
        return jsonify(result)
    return jsonify({'message': 'no course'}), 404


# 搜索课堂
@student.route('/search_class', methods=['GET', 'POST'])
@login_required
def search_class():
    data = request.form
    course_id = data.get('course_id')
    course = Course.query.filter_by(course_id=course_id).first()
    if course is None:
        return jsonify({'message': 'course not exists'}), 400
    else:
        print("课程" + course_id + "添加成功！")
        teach = Instructor.query.filter_by(id=course.teacher_id).first()
        return jsonify({'course_id': course_id,
                        'course_name': course.course_name,
                        'teacher_name': teach.name})


# 加入课堂
@student.route('/join_class', methods=['GET', 'POST'])
@login_required
def join_class():
    pass


# 退出课堂
@student.route('/quit_class', methods=['GET'])
@login_required
def quit_class():
    pass