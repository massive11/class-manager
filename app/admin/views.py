from ..models import *
from .. import db, app
from flask_login import login_required
from . import admin
from flask import jsonify, request
import json


@admin.route('/account_list')
@login_required
def account_list():
    all_accounts = Account.query.all()
    all_students = Student.query.filter(Student.id.in_([student.account for student in all_accounts
                                                        if student.type == 'student'])).all()
    result = [{'account': student.id, 'name': student.name, 'type': 'student'}
              for student in all_students]
    all_instructors = Instructor.query.filter(Instructor.id.in_([instructor.account for instructor in all_accounts
                                                                 if instructor.type == 'instructor']))
    result += [{'account': instructor.id, 'name': instructor.name, 'type': 'instructor'}
               for instructor in all_instructors]
    all_admins = Admin.query.filter(Admin.id.in_([admin.account for admin in all_accounts
                                                  if admin.type == 'admin']))
    result = result + [{'account': admin.id, 'name': admin.name, 'type': 'admin'}
                       for admin in all_admins]
    return jsonify(result)


@admin.route('/change_account', methods=['POST', 'GET'])
@login_required
def change_account():
    post_data = json.loads(request.data.decode())
    change_type = post_data.get('change_type')
    if change_type == 'DELETE':
        detail = post_data.get('detail')
        delete_account = Account.query.get(int(detail.get('account')))
        post_type = detail.get('type')
        try:
            if delete_account is not None:
                db.session.delete(delete_account)
                db.session.commit()
                if post_type == 'student':
                    delete_student = Student.query.get(int(detail.get('account')))
                    db.session.delete(delete_student)
                    db.session.commit()
                elif post_type == 'instructor':
                    delete_teacher = Instructor.query.get(int(detail.get('account')))
                    db.session.delete(delete_teacher)
                    db.session.commit()
                elif post_type == 'admin':
                    delete_admin = Admin.query.get(int(detail.get('account')))
                    db.session.delete(delete_admin)
                    db.session.commit()
                return jsonify({'message': 'delete ok'})
            else:
                return jsonify({'message': 'no account'}), 404
        except:
            return jsonify({'message': '请重新检查信息'}), 403
    if change_type == 'UPDATE':
        detail = post_data.get('detail')
        post_account = detail.get('account')
        if post_account is None:
            return jsonify({'message': 'no account'}), 401
        update_account = Account.query.filter_by(account=post_account).first()
        if update_account is None:
            return jsonify({'message': 'no account'}), 404
        post_type = detail.get('type', update_account.type)
        post_passwd = detail.get('passwd', update_account.password)
        update_account.password = post_passwd
        update_user = None
        if post_type == 'student':
            update_user = Student.query.filter_by(id=post_account).first()
        elif post_type == 'instructor':
            update_user = Instructor.query.filter_by(id=post_account).first()
        elif post_type == 'admin':
            update_user = Admin.query.filter_by(id=post_account).first()
        if update_user is not None:
            update_user.name = detail.get('name', update_user.name)
        else:
            return jsonify({'message': 'no user'}), 404
        db.session.add(update_account)
        db.session.add(update_user)
        db.session.commit()
        return jsonify({'message': 'update ok'})
    if change_type == 'INSERT':
        detail = post_data.get('detail')
        post_account = detail.get('account')
        post_name = detail.get('name')
        post_type = detail.get('type')
        post_passwd = detail.get('passwd')
        if post_account is None or post_type is None or post_name is None or post_passwd is None:
            return jsonify({'message': 'data missing'}), 403
        insert_account = Account(account=post_account, type=post_type, password=post_passwd)
        if post_type == 'student':
            insert_user = Student(id=post_account, name=post_name, year=detail.get('year', 2017))
            print(insert_user)
            db.session.add(insert_user)
            db.session.commit()
        elif post_type == 'instructor':
            insert_user = Instructor(id=post_account, name=post_name)
            db.session.add(insert_user)
            db.session.commit()
        elif post_type == 'admin':
            insert_user = Admin(id=post_account, name=post_name)
            db.session.add(insert_user)
            db.session.commit()
        db.session.add(insert_account)
        db.session.commit()
        return jsonify({'message': 'insert OK'})
