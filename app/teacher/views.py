from flask import current_app, request, jsonify, session
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import json


@teacher.route('/mine_class')
@login_required
def mine_class():
    mine_teachs = Course.query.filter_by(teacher_id=current_user.id).all()
    if len(mine_teachs) == 0:
        return jsonify({'message': 'no class'}), 404
    result = []
    for mine_cla in mine_teachs:
        course_id = mine_cla.course_id
        re = {'course_id': course_id,
              'course_name': mine_cla.course_name}
        result.append(re)
        print(result)
    return jsonify(result)


@teacher.route('/class_info')
@login_required
def tea_class():
    mine_teachs = Course.query.filter_by(teacher_id=current_user.id).all()
    if len(mine_teachs) == 0:
        return jsonify({'message': 'no class'}), 404
    result = []
    temp_re = {}
    for mine_cla in mine_teachs:
        temp_re[mine_cla.course_id] = {
            'course_id': mine_cla.course_id,
            'course_name': mine_cla.course_name
        }
    for keys in temp_re.keys():
        result.append(temp_re[keys])
    print(result)
    return jsonify(result)


@teacher.route('/class_people/<course_id>', methods=['GET'])
@login_required
def class_info(course_id):
    if course_id is None:
        return jsonify({'message': 'no data'}), 401
    print(course_id)
    teas = Course.query.filter_by(course_id=course_id).all()
    print(teas)
    if current_user.id not in [tea.teacher_id for tea in teas]:
        return jsonify({'message': 'you are not its teacher'}), 403
    student_infos = StuCourse.query.filter_by(course_id=course_id).all()
    result = []
    for student_info in student_infos:
        stu = Student.query.filter_by(id=student_info.uid).first()
        re = {'student_id': stu.id,
              'student_name': stu.name}
        result.append(re)
    print(result)
    return jsonify(result)


# 创建课程
@teacher.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    data = request.form
    teacher_id = current_user.id
    course_id = data.get('course_id')
    course_name = data.get('course_name')
    course = Course.query.filter_by(course_id=course_id).first()
    if course is None:
        course = Course(course_id=course_id, course_name=course_name, teacher_id=teacher_id)
        db.session.add(course)
        db.session.commit()
        print("课程" + course_name + "创建成功！")
        return jsonify({'message': 'create course'})
    else:
        return jsonify({'message': 'account exists'}), 400


# 删除课程
@teacher.route('/delete_course', methods=['GET', 'POST'])
@login_required
def delete_course():
    pass