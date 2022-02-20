import os
from dotenv import load_dotenv
from enum import Enum
import requests

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API")

class AVEndpoints(Enum):
    IncomeStatement = "https://www.alphavantage.co/query?function=INCOME_STATEMENT"
    CashFlow = "https://www.alphavantage.co/query?function=CASH_FLOW"
    BalanceSheet = "https://www.alphavantage.co/query?function=BALANCE_SHEET"





def get_balance_sheet(ticker: str) -> dict:
    try:
        params = {
            "apikey": API_KEY, 
            "symbol": ticker
        }
        response = requests.get(AVEndpoints.BalanceSheet.value, params=params)
        if response.status_code != 200:
            return f"Invalid response for get_balance_sheet: {response.reason}"
        return response.json()

    except Exception as e:
        print(f"get_balance_sheet raised exception: {e}")



def get_income_statement(ticker: str) -> dict:
    try:
        params = {
            "apikey": API_KEY, 
            "symbol": ticker
        }
        response = requests.get(AVEndpoints.IncomeStatement.value, params=params)
        if response.status_code != 200:
            return f"Invalid response for get_income_statement: {response.reason}"
        return response.json()
        
    except Exception as e:
        print(f"get_income_statement raised exception: {e}")




def get_cash_flow(ticker: str) -> dict:
    try:
        params = {
            "apikey": API_KEY, 
            "symbol": ticker
        }
        response = requests.get(AVEndpoints.CashFlow.value, params=params)
        if response.status_code != 200:
            return f"Invalid response for get_cash_flow: {response.reason}"
        return response.json()

    except Exception as e:
        print(f"get_cash_flow raised exception: {e}")


if __name__ == "__main__":
    ...