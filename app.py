from flask import Flask
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Account, StuCourse, Course, Student, Instructor, Admin, AnonymousUserMixin


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
