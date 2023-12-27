from flask import request, redirect, url_for, session
from flask_restx import Resource
from library.extension import db
from library.model import User
from library.marshmallow_model import UserSchema
from flask_login import login_user, logout_user, current_user, login_required
from functools import wraps
import bcrypt
import re


user_schema = UserSchema()
users_schema = UserSchema(many=True)

def guest_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            print("user has logged in")
        return f(*args, **kwargs)
    return decorated_function

class AddMultipleUserResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, list):
                return {"message": "Invalid data format. Expected a JSON array."}, 400

            added_records = []

            for item in data:
                if ("userName" in item) and ("password" in item) and ("email" in item):
                    name = item["userName"]
                    password = item["password"]
                    email = item["email"]
                    avtSrc = item.get("avtSrc", "")
                    firstName = item.get("firstName", "")
                    lastName = item.get("lastName", "")
                    institution = item.get("institution", "")

                    # Hash the password before storing it in the database
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                    try:
                        new_user = User(
                            userName=name,
                            password=hashed_password,
                            email=email,
                            avtSrc=avtSrc,
                            firstName=firstName,
                            lastName=lastName,
                            institution=institution
                        )
                        db.session.add(new_user)
                        added_records.append(new_user)
                    except Exception as e:
                        db.session.rollback()
                        return {"message": "Add user failed", "error": str(e)}, 400
                else:
                    return {"message": "Request error"}, 400

            db.session.commit()
            return {"message": "Users added successfully", "added_users": [user.id for user in added_records]}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while adding users.", "error": str(e)}, 500
        

class AddUserResource(Resource):
    def post(self):
        data = request.json
        if data and ("userName" in data) and ("password" in data) and ("email" in data):
            name = data["userName"]
            password = data["password"]
            email = data["email"]
            avtSrc = data.get("avtSrc", "")
            firstName = data.get("firstName", "")
            lastName = data.get("lastName", "")
            institution = data.get("institution", "")

            # Hash the password before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                new_user = User(
                    userName=name,
                    password=hashed_password,
                    email=email,
                    avtSrc=avtSrc,
                    firstName=firstName,
                    lastName=lastName,
                    institution=institution
                )
                db.session.add(new_user)
                db.session.commit()
                return {"message": "User added successfully!", "user": user_schema.dump(new_user)}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Add user failed", "error": str(e)}, 400
        else:
            return {"message": "Request error"}, 400

class GetUserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return user_schema.dump(user)
        else:
            return {"message": "User not found"}, 404
        
class GetCurrentSessionUser(Resource):
    def get(self):
        try:
            if current_user.is_authenticated:
                return user_schema.dump(current_user)
            else:
                return {"message": "No user currently in the session"}, 404
        except Exception as e:
            return {"message": "Error retrieving current session user", "error": str(e)}, 500 

class GetAllUsersResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

class UpdateUserResource(Resource):
    def put(self, user_id):
        user = User.query.get(user_id)

        if user:
            data = request.json
            if data and ("userName" in data) and ("email" in data):
                try:
                    user.userName = data["userName"]
                    user.email = data["email"]

                    if "password" in data:
                        # Update the password if it's provIDed in the request
                        password = data["password"]
                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                        user.password = hashed_password

                    db.session.commit()
                    return {"message": "User updated successfully!", "user": user_schema.dump(user)}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update user failed", "error": str(e)}, 400
            else:
                return {"message": "Request error"}, 400
        else:
            return {"message": "User not found"}, 404

class DeleteUserResource(Resource):
    def delete(self, id):
        user = User.query.get(id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                return {"message": "User deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Delete user failed"}, 400
        else:
            return {"message": "User not found"}, 404
        
class LoginUserResource(Resource):
    def post(self):
        data = request.json
        if "email" in data and "password" in data:
            email = data["email"]
            password = data["password"]
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                # Passwords match - log in the user
                login_user(user)
                print("User logged in:", current_user)
                return {"message": "Login successfully"}, 200
            else:
                return {"message": "Wrong password or user not found"}
        else:
            return {"message": "Request error"}, 400
        
         
class LogoutUserResource(Resource):
    def post(self):  
        db.session
        logout_user()
        return "Logged out successfully!"


class SignInUserResource(Resource):
    def post(self):
        data = request.json
        if "userName" in data and "password1" in data and "password2" in data and "email" in data:
            userName = data["userName"]
            password1 = data["password1"]
            password2 = data["password2"]
            email = data["email"]

            if userName == "" or password1 == "" or email == "":
                return {"message": "Please fulfill the form"}

            def email_valIDate(email):
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                if re.fullmatch(regex, email):
                    return True
                else:
                    return False

            if not email_valIDate(email):
                return {"message": "Email you've just typed in is not in the correct form"}

            if User.query.filter_by(email=email).first() or User.query.filter_by(userName=userName).first():
                return {"message": "Email or userName already exists"}

            if password1 == password2:
                hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                new_user = User(
                    userName=userName,
                    password=hashed_password,
                    email=email,
                    firstName="",
                    lastName="",
                    institution=""
                )
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    # Implement any additional logic for a successful signup here
                    return {"message": "User added successfully!"}, 201
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Add user failed"}
            else:
                return {"message": "Passwords do not match"}
        else:
            return {"message": "Request error"}
        
class UpdatePasswordResource(Resource):
    @login_required
    def put(self):
        data = request.json
        if "current_password" in data and "new_password" in data:
            current_password = data["current_password"]
            new_password = data["new_password"]

            # Check if the current password matches the user's actual password
            if bcrypt.checkpw(current_password.encode('utf-8'), current_user.password.encode('utf-8')):
                # Hash the new password before updating it in the database
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                
                # Update the user's password
                current_user.password = hashed_password
                
                try:
                    db.session.commit()
                    return {"message": "Password updated successfully!"}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update password failed", "error": str(e)}, 400
            else:
                return {"message": "Current password is incorrect"}, 401
        else:
            return {"message": "Request error"}, 400
        
class GetCurrentSessionUserResource(Resource):
    def get(self):
        try:
            # Check if a user is currently in session
            if current_user.is_authenticated:
                # Serialize the user data (adjust the serialization as per your model structure)
                user_data = {
                    "id": current_user.id,
                    "email": current_user.email,
                    "userName": current_user.userName,
                    "firstName": current_user.firstName,
                    "lastName": current_user.lastName,
                    "institution": current_user.institution,
                    "avtSrc": current_user.avtSrc
                }

                return {"user": user_data}, 200
            else:
                return {"message": "No user currently in session"}, 404
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500