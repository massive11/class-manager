from flask import current_app, request, jsonify, session
from ..models import *
from flask_login import current_user, login_required
from .. import app, db
from . import teacher
import json


# @teacher.route('/mine_class')
# @login_required
# def mine_class():
#     mine_teachs = Teach.query.filter_by(instructor_id=current_user.id).all()
#     if len(mine_teachs) == 0:
#         return jsonify({'message':'no class'}), 404
#     result = []
#     for mine_cla in mine_teachs:
#         class_id = mine_cla.class_id
#         re = {'class_id':class_id,
#               'course_id':mine_cla.classes.course.id,
#               'course_name':mine_cla.classes.course.name}
#         sch = Schedule.query.filter_by(class_id=class_id).first()
#         if sch is None:
#             return jsonify({'message':'data missing'}), 404
#         re['classroom_id'] = sch.classroom_id
#         re['day'] = sch.day
#         re['week'] = sch.week
#         re['section'] = sch.section
#         result.append(re)
#     return jsonify(result)