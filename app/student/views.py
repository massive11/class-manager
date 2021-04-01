from . import student
from .. import db, login_manager
from ..models import *
from flask import request, jsonify
from flask_login import current_user, login_required,login_manager
from datetime import datetime
login_manager.login_view = 'main.no_login'


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
                  'instructor_name': tea.name
                  }
            result.append(re)
        return jsonify(result)
    return jsonify({'message': 'no course'}), 404