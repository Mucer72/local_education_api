from flask import Blueprint
from .services import *

UserProgress = Blueprint("UserProgress", __name__)

@UserProgress.route("/userprogress/add", methods=["POST"])
def add_UserProgress():
    add_UserProgress_resource = AddUserProgressResource()
    return add_UserProgress_resource.post()

@UserProgress.route("/userprogress/get/<int:id>", methods=["GET"])
def get_UserProgress(id):
    get_UserProgress_resource = GetUserProgressByIDResource()
    return get_UserProgress_resource.get(id)

@UserProgress.route("/userprogress/get-all", methods=["GET"])
def get_UserProgresss():
    get_all_UserProgresss_resource = GetAllUserProgressesResource()
    return get_all_UserProgresss_resource.get()

@UserProgress.route("/userprogress/delete/<int:id>", methods=["DELETE"])
def delete_UserProgress(id):
    delete_UserProgress_resource = DeleteUserProgressResource()
    return delete_UserProgress_resource.delete(id)

@UserProgress.route("/userprogress/update", methods=["PUT"])
def update_Current_UserProgress(topic_id):
    update_Current_UserProgress_resource = UpdateUserProgressResource()
    return update_Current_UserProgress_resource.put(topic_id)

@UserProgress.route("/userprogress/get-user-score", methods=["GET"])
@login_required
def get_user_score():
    get_user_score_resource = GetUserScoreResource()
    return get_user_score_resource.get()

@UserProgress.route("/user-progress/update-score/<int:topic_id>/<int:new_score>", methods=["PUT"])
@login_required
def update_user_progress_score(topic_id, new_score):
    update_user_progress_score_resource = UpdateUserProgressScoreResource()
    return update_user_progress_score_resource.put(topic_id, new_score)