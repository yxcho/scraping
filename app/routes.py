from flask import Flask
from flask_restful import Api
from app.mod_controllers.testController import TestController
app = Flask(__name__)
api = Api(app)
api.add_resource(TestController, '/test')
