from flask import Blueprint
from .services import *


Part = Blueprint("Part",__name__)

@Part.route("/part/add", methods=["POST"])
def add_part():
    add_part_resource = AddPartResource()
    return add_part_resource.post()

@Part.route("/part/get/<int:id>", methods=["GET"])
def get_part(id):
    get_part_resource = GetPartByIDResource()
    return get_part_resource.get(id)

@Part.route("/part/get-all", methods=["GET"])
def get_parts():
    get_all_parts_resource = GetAllPartsResource()
    return get_all_parts_resource.get()


@Part.route("/part/update/<int:id>", methods=["PUT"])
def update_part(id):
    update_part_resource = UpdatePartResource()
    return update_part_resource.put(id)

@Part.route("/part/delete/<int:id>", methods=["DELETE"])
def delete_part(id):
    delete_part_resource = DeletePartResource()
    return delete_part_resource.delete(id)

@Part.route("/part/update-all-view-status", methods=["PUT"])
def update_all_parts_view_status():
    update_all_parts_view_status_resource = UpdateAllPartsViewStatusResource()
    return update_all_parts_view_status_resource.put()

@Part.route("/part/check-all-view-status/<int:topic_id>", methods=["GET"])
def check_all_parts_view_status(topic_id):
    check_all_parts_view_status_resource = CheckAllPartsViewStatusResource()
    return check_all_parts_view_status_resource.get(topic_id)

@Part.route("/topic/get-parts-by-topicid/<int:topic_id>", methods=["GET"])
def get_all_parts(topic_id):
    get_all_parts_resource = GetPartsByTopicIDResource()
    return get_all_parts_resource.get(topic_id)