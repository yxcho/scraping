import os
from dotenv import load_dotenv
from enum import Enum
import requests

load_dotenv()

API_KEY = os.getenv("RAPID_API_KEY")

class RapidAPIEndpoints(Enum):
    Statistics = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"




def get_statistics(ticker: str) -> dict:
    try:
        header = {
            "x-rapidapi-host": "yh-finance.p.rapidapi.com", 
            "x-rapidapi-key": API_KEY
        }
        params = {
            "symbol": ticker
        }
        response = requests.get(RapidAPIEndpoints.Statistics.value, headers=header, params=params)
        if response.status_code != 200:
            return f"Invalid response for get_statistics: {response.reason}"
        return response.json()

    except Exception as e:
        print(f"get_statistics raised exception: {e}")




if __name__ == "__main__":
    print(get_statistics("GOOGL"))