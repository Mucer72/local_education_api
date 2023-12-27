from flask import Blueprint
from .services import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
User = Blueprint("User", __name__)

@User.route("/user/add-multi", methods=["POST"])
def add_multi_user():
    add_multi_user_resource = AddMultipleUserResource()
    return add_multi_user_resource.post()

@User.route("/user/add", methods=["POST"])
def add_user():
    add_user_resource = AddUserResource()
    return add_user_resource.post()

@User.route("/user/get/<int:id>", methods=["GET"])
def get_user(id):
    get_user_resource = GetUserResource()
    return get_user_resource.get(id)

@User.route("/user/get/session", methods=["GET"])
def get_current_user():
    get_current_user_resource = GetCurrentSessionUser()
    return get_current_user_resource.get()

@User.route("/user/get-all", methods=["GET"])
def get_users():
    get_all_users_resource = GetAllUsersResource()
    return get_all_users_resource.get()

@User.route("/user/update/<int:id>", methods=["PUT"])
def update_user(id):
    update_user_resource = UpdateUserResource()
    return update_user_resource.put(id)

@User.route("/user/delete/<int:id>", methods=["DELETE"])
def delete_user(id):
    delete_user_resource = DeleteUserResource()
    return delete_user_resource.delete(id)

@User.route("/user/login", methods=["POST"])
@guest_required
def login_user():
    login_user_resource = LoginUserResource()
    return login_user_resource.post()

@User.route("/user/signup", methods=["POST"])
@guest_required
def signin_user():
    signin_user_resource = SignInUserResource()
    return signin_user_resource.post()

@User.route("/user/logout", methods=["POST"])
@login_required
def logout_user():
    logout_user_resource = LogoutUserResource()
    return logout_user_resource.post()

@User.route("/user/update-password", methods=["PUT"])
@login_required
def update_password():
    update_password_resource = UpdatePasswordResource()
    return update_password_resource.put()

@User.route("/user/get-session", methods=["GET"])
def get_current_session_user():
    get_current_session_user_resource = GetCurrentSessionUserResource()
    return get_current_session_user_resource.get()