from .. import app, db, login_manager
from flask import request, current_app, jsonify, make_response
from ..models import Account, Student, Course, StuCourse, Admin, Instructor, AnonymousUser
from flask_login import login_user, logout_user, current_user, login_required
from . import main
import json

login_manager.login_view = 'main.no_login'


@main.route('/')
def hello():
    return 'hello world'


@main.route('/no_login')
def no_login():
    return "no login", 401


@main.route('/login', methods=['POST', 'GET'])
def login():
    data = request.form
    account = data.get('account')
    password = data.get('password')
    remember_me = True
    if account is None or password is None or remember_me is None:
        return jsonify({'message': 'data missing'}), 400
    user = Account.query.filter_by(account=account).first()
    if user is not None:
        if user.password == password:
            if user.type == 'student':
                s = Student.query.filter_by(id=account).first()
                login_user(s, remember=remember_me)
                print("Hello "+current_user.id)
                return jsonify({'type': 'student'})
            if user.type == 'instructor':
                i = Instructor.query.filter_by(id=account).first()
                login_user(i, remember=remember_me)
                return jsonify({'type': 'instructor'})
            if user.type == 'admin':
                a = Admin.query.filter_by(id=account).first()
                login_user(a, remember=remember_me)
                return jsonify({'type': 'admin'})
            if account in app.config['FLASKY_ADMIN']:
                login_user(user, remember=remember_me)
                return jsonify({'type': 'root'})
            return jsonify({'message': 'type error'}), 400
        return jsonify({'message': 'password error'}), 403
    return jsonify({'message': 'no account'}), 404


@main.route('/register', methods=['POST'])
def register():
    data = request.form
    account = data.get('account')
    name = data.get('name')
    password = data.get('password')
    user = Account.query.filter_by(account=account).first()
    if user is None:
        user = Account(account=account, password=password, type='student')
        u = Student(id=account, name=name, answer=0, present=0)
        db.session.add(user)
        db.session.add(u)
        db.session.commit()
        print("用户"+account+"注册成功！")
        return jsonify({'type': 'student'})
    else:
        return jsonify({'message': 'account exists'}), 400


@main.route('/who_am_i', methods=['GET'])
@login_required
def who_am_i():
    return jsonify({"type": Account.query.filter_by(account=current_user.id).first().type,
                    "name": current_user.name})


@main.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'logout successful'})


@main.route('/change_passwd', methods=['GET', 'POST'])
@login_required
def change_passwd():
    data = request.form
    u_account = Account.query.filter_by(account=current_user.id).first()
    old_password = u_account.password
    if old_password is None:
        return jsonify({'message': 'no account'}), 404
    if old_password == data.get('old_password'):
        u_account.password = data['new_password']
        db.session.add(u_account)
        db.session.commit()
        return jsonify({'message': 'change successful'})
    else:
        return jsonify({'message': 'password error'}), 403




