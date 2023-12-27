from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from .extension import db, marshmallow
from library.model import User as UserModel
from .User.controller import User
from .Topic.controller import Topic
from .UserProgress.controller import UserProgress
from .Part.controller import Part
from .Type.controller import Type
import os
import pymysql

pymysql.install_as_MySQLdb()

def create_database(app):
    with app.app_context():
        db.create_all()
    print("Database created")

def create_app(config_file="config.py"):
    app = Flask(__name__)
    
    #CORS(app, origins="http://localhost:58071", supports_credentials=True)
    CORS(app, supports_credentials=True)
    app.secret_key = 'secret'
    login_manager = LoginManager()
    login_manager.init_app(app)

    marshmallow.init_app(app)

    app.config.from_pyfile(config_file)
    app.config['SESSION_TYPE'] = 'filesystem'

    db.init_app(app)
    create_database(app)  # Call the database creation function here
    app.register_blueprint(User)
    app.register_blueprint(UserProgress)
    app.register_blueprint(Topic)
    app.register_blueprint(Type)
    app.register_blueprint(Part)


    @app.route('/', methods=['GET'])
    def loginCheck():
        print("User logged in:", current_user)
        if current_user.is_authenticated:
            print("User is authenticated:", current_user)
            return {"loginstatus":True}
        else: 
            print("User is not authenticated")
            return {"loginstatus":False}


    @login_manager.user_loader
    def load_user(user_id):
        user = UserModel.query.get(user_id)
        return user
    return app

