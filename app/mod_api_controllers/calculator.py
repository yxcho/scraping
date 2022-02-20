from flask_restful import Resource, request
from app.mod_general import calculator



# follow this JSON response format:
# https://github.com/omniti-labs/jsend
class CalculatorController(Resource):
    def get(self):
        try:
            params = request.args
            ticker = params.get("ticker", None)
            if ticker:
                response = calculator.calculate_iv(ticker.upper())
                status = "success"
            else:
                status = "fail"
                response = {"url": "ticker symbol is not provided"}
            return {"status": status, "data": response}, 200

        except Exception as e:
            msg = f"CalculatorController endpoint raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204

