from flask import request
from flask_restx import Resource
from library.extension import db
from library.model import UserProgress
from library.marshmallow_model import UserProgressSchema
from flask_login import current_user, login_required
from sqlalchemy import func

user_progress_schema = UserProgressSchema()
user_progresses_schema = UserProgressSchema(many=True)

class AddUserProgressResource(Resource):
    def post(self):
        data = request.json
        if data and ("userID" in data) and ("topicID" in data) and ("score" in data):
            user_ID = data["userID"]
            topic_ID = data["topicID"]
            score = data["score"]

            try:
                new_user_progress = UserProgress(
                    userID=user_ID,
                    topicID=topic_ID,
                    score=score
                )
                db.session.add(new_user_progress)
                db.session.commit()
                return {"message": "UserProgress added successfully!"}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Add UserProgress failed", "error": str(e)}, 400
        else:
            return {"message": "Request error"}, 400

class GetAllUserProgressesResource(Resource):
    def get(self):
        user_progresses = UserProgress.query.all()
        return user_progresses_schema.dump(user_progresses)

class GetUserProgressByIDResource(Resource):
    def get(self, ID):
        user_progress = UserProgress.query.get(ID)
        if user_progress:
            return user_progress_schema.dump(user_progress)
        else:
            return {"message": "UserProgress not found"}, 404

class UpdateUserProgressResource(Resource):
    def put(self, id):
        user_progress = UserProgress.query.get(id)
        if user_progress:
            data = request.json
            if data and ("userID" in data) and ("topicID" in data) and ("score" in data):
                try:
                    user_progress.userID = data["userID"]
                    user_progress.topicID = data["topicID"]
                    user_progress.score = data["score"]

                    db.session.commit()
                    return {"message": "UserProgress updated successfully!"}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update UserProgress failed", "error": str(e)}, 400
            else:
                return {"message": "Request error"}, 400
        else:
            return {"message": "UserProgress not found"}, 404

class DeleteUserProgressResource(Resource):
    def delete(self, ID):
        user_progress = UserProgress.query.get(ID)
        if user_progress:
            try:
                db.session.delete(user_progress)
                db.session.commit()
                return {"message": "UserProgress deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Delete UserProgress failed", "error": str(e)}, 400
        else:
            return {"message": "UserProgress not found"}, 404
        
class GetUserScoreResource(Resource):
    @login_required
    def get(self):
        user_progress = UserProgress.query.filter_by(userID=current_user.id).first()

        if user_progress:
            return {"user_score": user_progress.score}, 200
        else:
            return {"message": "User progress not found"}, 404

class UpdateUserProgressScoreResource(Resource):
    def put(self, topic_id, new_score):
        try:
            # Check if a user is currently in session
            if current_user.is_authenticated:
                # Check if the UserProgress record exists for the current user and topic_id
                user_progress = UserProgress.query.filter_by(userID=current_user.id, topicID=topic_id).first()

                if user_progress:
                    # Update the score
                    user_progress.score = new_score
                    db.session.commit()

                    return {"message": "UserProgress score updated successfully!"}, 200
                else:
                    return {"message": "UserProgress record not found"}, 404
            else:
                return {"message": "No user currently in session"}, 401
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500