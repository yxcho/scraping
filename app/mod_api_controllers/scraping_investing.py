from flask_restful import Resource, request
from app.mod_data_extraction import investingdotcom

# follow this JSON response format:
# https://github.com/omniti-labs/jsend
class InvestingDotCom(Resource):
    def get(self):
        try:
            data = request.json
            investing_dotcom_url = data["ratio_url"]
            if investing_dotcom_url:
                ratios = investingdotcom.get_ratios(investing_dotcom_url)
                status = "success"
            else:
                status = "fail"
                ratios = {"url": "URL is not provided"}
            return {"status": status, "data": ratios}, 200

        except Exception as e:
            msg = f"InvestingDotCom API class raised exception: {e}"
            print(msg)
            return {"status": "error", "message": msg}, 204

