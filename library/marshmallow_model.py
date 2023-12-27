from .extension import marshmallow
from marshmallow import Schema, fields

class UserSchema(Schema):
    class Meta:
        fields = ('id', 'email', 'password', 'userName', 'firstName', 'lastName', 'institution', 'avtSrc')

    id = fields.Integer(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    userName = fields.String(required=True)
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    institution = fields.String(required=True)
    avtSrc = fields.String()

class UserProgressSchema(Schema):
    class Meta:
        fields = ('userID', 'topicID', 'score')

    userID = fields.Integer(required=True)
    topicID = fields.Integer(required=True)
    score = fields.Integer(required=True)

class TopicSchema(Schema):
    class Meta:
        fields = ('id', 'title', 'description')

    id = fields.Integer(required=True)
    title = fields.String(required=True)
    description = fields.String(required=True)

class PartSchema(Schema):
    class Meta:
        fields = ('id', 'topicID', 'viewStatus', 'title')

    id = fields.Integer(required=True)
    topicID = fields.Integer(required=True)
    viewStatus = fields.Boolean(required=True)
    title = fields.String(required=True)

class TypeSchema(Schema):
    class Meta:
        fields = ('type', 'partID', 'topicID', 'mediaPath', 'content', 'viewStatus')

    type = fields.Integer(required=True)
    partID = fields.Integer(required=True)
    topicID = fields.Integer(required=True)
    mediaPath = fields.Dict()
    content = fields.Dict()
    viewStatus = fields.Boolean(required=True)
