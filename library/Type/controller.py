from flask import Blueprint
from .services import *


Type = Blueprint("Type",__name__)

@Type.route("/type/add", methods=["POST"])
def add_Type():
    add_Type_resource = AddTypeResource()
    return add_Type_resource.post()

@Type.route("/type/get/<int:id>", methods=["GET"])
def get_Type(id):
    get_Type_resource = GetTypeByIDResource()
    return get_Type_resource.get(id)

@Type.route("/type/get-all", methods=["GET"])
def get_Types():
    get_all_Types_resource = GetAllTypesResource()
    return get_all_Types_resource.get()

@Type.route("/type/update/<int:id>", methods=["PUT"])
def update_Type(id):
    update_Type_resource = UpdateTypeResource()
    return update_Type_resource.put(id)

@Type.route("/type/delete/<int:id>", methods=["DELETE"])
def delete_Type(id):
    delete_Type_resource = DeleteTypeResource()
    return delete_Type_resource.delete(id)

@Type.route("/type/update-view-status/<int:topic_id>/<int:part_id>", methods=["PUT"])
def update_type_view_status(topic_id, part_id):
    update_type_view_status_resource = UpdateTypeViewStatusResource()
    return update_type_view_status_resource.put(topic_id, part_id)

@Type.route("/type/get-type/<int:topic_id>/<int:part_id>", methods=["GET"])
def get_type(topic_id, part_id):
    get_type_resource = GetTypeResource()
    return get_type_resource.get(topic_id, part_id)