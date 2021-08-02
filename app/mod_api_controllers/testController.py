from flask_restful import Resource, request


class TestController(Resource):
    def get(self):
        return {
            "message": "get: hello from the testcontroller"
        }
