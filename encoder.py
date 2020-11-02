from flask.json import JSONEncoder
from bson import ObjectId

class MongoEncoder(JSONEncoder):
    """
    Custom encoder class with the ability to serialize
    MongoDB's ObjectId type.
    """

    def default(self, obj):
        """
        Encodes items of type ObjectId with its str() value.
        """
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)
