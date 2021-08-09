from flask_restful import Api
from app.mod_api_controllers.testController import TestController
from app.mod_api_controllers.dataScraping import InvestingDotCom
from app import app
api = Api(app)


api.add_resource(TestController, '/test')
api.add_resource(InvestingDotCom, '/data/collect/investingdotcom')
