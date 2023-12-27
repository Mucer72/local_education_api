from flask import request
from flask_restx import Resource
from library.extension import db
from library.model import Type
from library.marshmallow_model import TypeSchema

import os
from dotenv import load_dotenv

load_dotenv()

type_schema = TypeSchema()
types_schema = TypeSchema(many=True)

class AddTypeResource(Resource):
    def post(self):
        data = request.json
        if data and ("type" in data) and ("partID" in data) and ("topicID" in data) and ("mediaPath" in data) and ("content" in data) and ("viewStatus" in data):
            type_val = data["type"]
            part_ID = data["partID"]
            topic_ID = data["topicID"]
            media_path = data["mediaPath"]
            content = data["content"]
            view_status = data["viewStatus"]

            try:
                new_type = Type(
                    type=type_val,
                    partID=part_ID,
                    topicID=topic_ID,
                    mediaPath=media_path,
                    content=content,
                    viewStatus=view_status
                )
                db.session.add(new_type)
                db.session.commit()
                return {"message": "Type added successfully!"}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Add Type failed", "error": str(e)}, 400
        else:
            return {"message": "Request error"}, 400

class GetAllTypesResource(Resource):
    def get(self):
        types = Type.query.all()
        return types_schema.dump(types)

class GetTypeByIDResource(Resource):
    def get(self, ID):
        type_item = Type.query.get(ID)
        if type_item:
            return type_schema.dump(type_item)
        else:
            return {"message": "Type not found"}, 404

class UpdateTypeResource(Resource):
    def put(self, ID):
        type_item = Type.query.get(ID)
        if type_item:
            data = request.json
            if data and ("partID" in data) and ("topicID" in data) and ("mediaPath" in data) and ("content" in data) and ("viewStatus" in data):
                try:
                    type_item.partID = data["partID"]
                    type_item.topicID = data["topicID"]
                    type_item.mediaPath = data["mediaPath"]
                    type_item.content = data["content"]
                    type_item.viewStatus = data["viewStatus"]

                    db.session.commit()
                    return {"message": "Type updated successfully!"}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update Type failed", "error": str(e)}, 400
            else:
                return {"message": "Request error"}, 400
        else:
            return {"message": "Type not found"}, 404

class DeleteTypeResource(Resource):
    def delete(self, ID):
        type_item = Type.query.get(ID)
        if type_item:
            try:
                db.session.delete(type_item)
                db.session.commit()
                return {"message": "Type deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Delete Type failed", "error": str(e)}, 400
        else:
            return {"message": "Type not found"}, 404

class UpdateTypeViewStatusResource(Resource):
    def put(self, topic_id, part_id):
        try:
            # Check if the Type with the given topic_id and part_id exists
            type_instance = Type.query.filter_by(topicID=topic_id, partID=part_id).first()

            if type_instance:
                # Update the viewStatus of the Type if it's not already true
                if not type_instance.viewStatus:
                    type_instance.viewStatus = True
                    db.session.commit()

                return {"message": "Type viewStatus updated successfully!"}, 200
            else:
                return {"message": "Type not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"An error occurred: {str(e)}"}, 500

class GetTypeResource(Resource):
    def get(self, topic_id, part_id):
        try:
            # Retrieve the Type with the given topic_id and part_id
            type_instance = Type.query.filter_by(topicID=topic_id, partID=part_id).first()

            if type_instance:
                # Serialize the type data (adjust the serialization as per your model structure)
                type_data = {
                    "type": type_instance.type,
                    "mediaPath": type_instance.mediaPath,
                    "content": type_instance.content,
                    "viewStatus": type_instance.viewStatus
                }

                return {"type": type_data}, 200
            else:
                return {"message": "Type not found"}, 404
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500