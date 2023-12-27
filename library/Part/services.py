from flask import request
from flask_restx import Resource
from library.extension import db
from library.model import Part, Type
from library.marshmallow_model import PartSchema

import os
from dotenv import load_dotenv

load_dotenv()

part_schema = PartSchema()
parts_schema = PartSchema(many=True)

class AddPartResource(Resource):
    def post(self):
        data = request.json
        if data and ("id" in data) and ("topicID" in data) and ("viewStatus" in data) and ("title" in data):
            part_ID = data["id"]
            topic_ID = data["topicID"]
            view_status = data["viewStatus"]
            title = data["title"]

            try:
                new_part = Part(
                    id=part_ID,
                    topicID=topic_ID,
                    viewStatus=view_status,
                    title=title
                )
                db.session.add(new_part)
                db.session.commit()
                return {"message": "Part added successfully!"}, 201
            except Exception as e:
                db.session.rollback()
                return {"message": "Add Part failed", "error": str(e)}, 400
        else:
            return {"message": "Request error"}, 400

class GetAllPartsResource(Resource):
    def get(self):
        parts = Part.query.all()
        return parts_schema.dump(parts)

class GetPartByIDResource(Resource):
    def get(self, id):
        part = Part.query.get(id)
        if part:
            return part_schema.dump(part)
        else:
            return {"message": "Part not found"}, 404

class UpdatePartResource(Resource):
    def put(self, id):
        part = Part.query.get(id)
        if part:
            data = request.json
            if data and ("topicID" in data) and ("viewStatus" in data) and ("title" in data):
                try:
                    part.topicID = data["topicID"]
                    part.viewStatus = data["viewStatus"]
                    part.title = data["title"]

                    db.session.commit()
                    return {"message": "Part updated successfully!"}, 200
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Update Part failed", "error": str(e)}, 400
            else:
                return {"message": "Request error"}, 400
        else:
            return {"message": "Part not found"}, 404

class DeletePartResource(Resource):
    def delete(self, id):
        part = Part.query.get(id)
        if part:
            try:
                db.session.delete(part)
                db.session.commit()
                return {"message": "Part deleted"}, 200
            except Exception as e:
                db.session.rollback()
                return {"message": "Delete Part failed", "error": str(e)}, 400
        else:
            return {"message": "Part not found"}, 404
        
class UpdateAllPartsViewStatusResource(Resource):
    def put(self):
        parts = Part.query.all()

        for part in parts:
            # Check if there are any Type instances with viewStatus=True for the current Part
            has_visible_types = Type.query.filter_by(partID=part.id, viewStatus=True).first() is not None

            # Update the viewStatus of the current Part based on the presence of visible Types
            part.viewStatus = has_visible_types

        try:
            db.session.commit()
            return {"message": "All Parts viewStatus updated successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Update All Parts viewStatus failed", "error": str(e)}, 400
        
class CheckAllPartsViewStatusResource(Resource):
    def get(self, topic_id):
        try:
            # Check if all parts with the given topic_id have viewStatus=True
            all_parts_visible = all(
                part.viewStatus for part in Part.query.filter_by(topicID=topic_id).all()
            )
            return {"all_parts_visible": all_parts_visible}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        
class GetPartsByTopicIDResource(Resource):
    def get(self, topic_id):
        try:
            # Retrieve all parts with the given topic_id
            parts = Part.query.filter_by(topicID=topic_id).all()

            # Serialize the parts data (adjust the serialization as per your model structure)
            parts_data = [{"id": part.id, "title": part.title, "viewStatus": part.viewStatus} for part in parts]

            return {"parts": parts_data}, 200
        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500