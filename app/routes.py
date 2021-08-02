from flask_restful import Api
from app.mod_controllers.testController import TestController
from app import app
api = Api(app)


api.add_resource(TestController, '/test')
