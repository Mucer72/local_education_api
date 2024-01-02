from flask import request
from flask_restx import Resource
from library.extension import db
from library.model import Topic
from library.marshmallow_model import TopicSchema

import os
from dotenv import load_dotenv

load_dotenv()

topic_schema = TopicSchema()
topics_schema = TopicSchema(many=True)

class AddTopicResource(Resource):
    def post(self):
        data = request.json
        if data and ("title" in data) and ("description" in data):
            title = data["title"]
            description = data["description"]

            try:
                new_topic = Topic(
                    title=title,
                    description=description
                )
                db.session.add(new_topic)
                db.session.commit()
                return {"message": "Topic added successfully!"}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Add Topic failed", "error": str(e)}, 400
        else:
            return {"message": "Request error"}, 400

class GetAllTopicsResource(Resource):
    def get(self):
        topics = Topic.query.all()
        return topics_schema.dump(topics)

class GetTopicByIDResource(Resource):
    def get(self, id):
        topic = Topic.query.get(id)
        if topic:
            return topic_schema.dump(topic)
        else:
            return {"message": "Topic not found"}, 404

class UpdateTopicResource(Resource):
    def put(self, id):
        topic = Topic.query.get(id)
        if topic:
            data = request.json
            if data and ("title" in data) and ("description" in data):
                try:
                    topic.title = data["title"]
                    topic.description = data["description"]

                    db.session.commit()
                    return {"message": "Topic updated successfully!"}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update Topic failed", "error": str(e)}, 400
            else:
                return {"message": "Request error"}, 400
        else:
            return {"message": "Topic not found"}, 404

class DeleteTopicResource(Resource):
    def delete(self, id):
        topic = Topic.query.get(id)
        if topic:
            try:
                db.session.delete(topic)
                db.session.commit()
                return {"message": "Topic deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Delete Topic failed", "error": str(e)}, 400
        else:
            return {"message": "Topic not found"}, 404
        
