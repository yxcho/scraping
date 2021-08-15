from flask_restful import Resource, request
from app.mod_data_extraction import yahoo_finance
from app.mod_general.static_variables import FinancialStatement
from pandas import DataFrame as df
import json

class Analysis(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                ratios = yahoo_finance.get_analysis(ticker)
                status = "success"
            else:
                status = "fail"
                ratios = {"url": "URL is not provided"}
            return {"status": status, "data": ratios}, 200

        except Exception as e:
            msg = f"Yahoo Finance Analysis API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204


class CashFlow(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                result = yahoo_finance.get_financials(ticker, FinancialStatement.CF.value)
                status = "success"
            else:
                status = "fail"
                result = {"url": "URL is not provided"}
            return {"status": status, "data": result}, 200

        except Exception as e:
            msg = f"Yahoo Finance Financials CashFlow API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204

class BalanceSheet(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                result = yahoo_finance.get_financials(ticker, FinancialStatement.BS.value)
                result = result.to_json()
                status = "success"
            else:
                status = "fail"
                result = {"url": "URL is not provided"}
            return {"status": status, "data": result}, 200

        except Exception as e:
            msg = f"Yahoo Finance Financials BalanceSheet API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204

class IncomeStatement(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                result = yahoo_finance.get_financials(ticker, FinancialStatement.IS.value)
                result = result.to_json()
                status = "success"
            else:
                status = "fail"
                result = {"url": "URL is not provided"}
            return {"status": status, "data": result}, 200

        except Exception as e:
            msg = f"Yahoo Finance Financials IncomeStatement API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204


class KeyStatistics(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                ratios = yahoo_finance.get_statistics(ticker)
                status = "success"
            else:
                status = "fail"
                ratios = {"url": "URL is not provided"}
            return {"status": status, "data": ratios}, 200

        except Exception as e:
            msg = f"Yahoo Finance Analysis Statistics API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204


class StockPrice(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                ratios = yahoo_finance.get_stock_prices(ticker)
                status = "success"
            else:
                status = "fail"
                ratios = {"url": "URL is not provided"}
            return {"status": status, "data": ratios}, 200

        except Exception as e:
            msg = f"Yahoo Finance Analysis StockPrice API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204
