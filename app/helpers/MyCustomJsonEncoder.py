"""
    This Json Encoder class will help us converting easily BSON object into JSON and so on
"""


from datetime import datetime, date
from bson import ObjectId, json_util
from json import JSONEncoder
from werkzeug.routing import BaseConverter


class MongoDbJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json_util.default(obj)
       


class ObjectIdConverter(BaseConverter):
    def to_myobj(self, value):
        return ObjectId(value)

    def to_url(self, value):
        return str(value)