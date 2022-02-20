from flask_restful import Api
from app.mod_api_controllers.testController import TestController
from app.mod_api_controllers.calculator import CalculatorController
from app.mod_api_controllers.scraping_investing import InvestingDotCom
from app.mod_api_controllers.scraping_yahoo import Analysis, BalanceSheet, StockPrice, CashFlow, IncomeStatement, KeyStatistics
from app.mod_api_controllers.scraping_finviz import Statistics
from app import app
api = Api(app)


api.add_resource(TestController, '/test')
api.add_resource(CalculatorController, '/calculate-iv/dcf')
api.add_resource(InvestingDotCom, '/data/collect/investingdotcom')
api.add_resource(Analysis, '/data/collect/yahoo/analysis')
api.add_resource(CashFlow, '/data/collect/yahoo/financials/cash-flow')
api.add_resource(BalanceSheet, '/data/collect/yahoo/financials/balance-sheet')
api.add_resource(IncomeStatement, '/data/collect/yahoo/financials/cash-flow')
api.add_resource(KeyStatistics, '/data/collect/yahoo/key-statistics')
api.add_resource(StockPrice, '/data/collect/yahoo/stockprice')
api.add_resource(Statistics, '/data/collect/finviz/statistics')
