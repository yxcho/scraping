from flask_restful import Resource, request
from app.mod_data_extraction import finviz

# follow this JSON response format:
# https://github.com/omniti-labs/jsend
class Statistics(Resource):
    def get(self):
        try:
            data = request.json
            ticker = data["ticker"].upper()
            if ticker:
                ratios = finviz.get_statistics(ticker)
                status = "success"
            else:
                status = "fail"
                ratios = {"url": "URL is not provided"}
            return {"status": status, "data": ratios}, 200

        except Exception as e:
            msg = f"Finviz API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204

