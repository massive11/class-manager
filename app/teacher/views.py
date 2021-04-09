from flask import current_app, request, jsonify, session
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import random


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
              'student_name': stu.name,
              'student_answer': stu.answer,
              'student_present': stu.present}
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
        return jsonify({'message': 'course exists'}), 400


# 随机点名
@teacher.route('/get_name', methods=['GET', 'POST'])
@login_required
def get_name():
    data = request.form
    course_id = data.get('course_id')
    print("course_id为："+course_id)
    stus = StuCourse.query.filter_by(course_id=course_id).all()
    print(stus)
    if len(stus) > 0:
        s = random.randint(1, len(stus))
        a = 0
        for stu in stus:
            a += 1
            if a == s:
                stu_id = stu.uid
                student = Student.query.filter_by(id=stu_id).first()
                return jsonify({'name': student.name})
    else:
        return jsonify({'message': 'no student'}), 400


# 创建课程
@teacher.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    data = request.form
    student_id = data.get('student_id')
    student_answer = data.get('student_answer')
    student_present = data.get('student_present')
    student = Student.query.filter_by(id=student_id).first()
    print(student_id)
    if student is not None:
        student.answer = student_answer
        student.present = student_present
        db.session.commit()
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'something error'}), 400