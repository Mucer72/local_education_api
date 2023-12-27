from flask import Blueprint
from .services import *


Topic = Blueprint("Topic",__name__)

@Topic.route("/topic/add", methods=["POST"])
def add_Topic():
    add_topic_resource = AddTopicResource()
    return add_topic_resource.post()

@Topic.route("/topic/get/<int:id>", methods=["GET"])
def get_Topic(id):
    get_topic_resource = GetTopicByIDResource()
    return get_topic_resource.get(id)

@Topic.route("/topic/get-all", methods=["GET"])
def get_Topics():
    get_all_topics_resource = GetAllTopicsResource()
    return get_all_topics_resource.get()

@Topic.route("/topic/update/<int:id>", methods=["PUT"])
def update_Topic(id):
    update_topic_resource = UpdateTopicResource()
    return update_topic_resource.put(id)

@Topic.route("/topic/delete/<int:id>", methods=["DELETE"])
def delete_Topic(id):
    delete_topic_resource = DeleteTopicResource()
    return delete_topic_resource.delete(id)