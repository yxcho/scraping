import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import string
from app.mod_general import common_functions
# pd.options.display.float_format = '{:.0f}'.format

FINVIZ_TABLE_ROW = 12
FINVIZ_TABLE_COL = 12

def get_statistics(ticker: str) -> dict:
    try:
        is_link = f'https://finviz.com/quote.ashx?t={ticker}'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(is_link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        statistics = {}

        features = soup.find_all('tr', class_='table-dark-row')
        if len(features) == 0:
            return None
            
        features = features[:FINVIZ_TABLE_ROW]

        for row in range(len(features)):
            colCount = len(features[row])

            for col in range(1, colCount, 3):
                name = features[row].contents[col].text
                value = common_functions.convert_to_digits(features[row].contents[col+1].text)
                statistics[name] = value
                print(f"{name: <20} - {value: <20}")
        driver.close()
        return statistics

    except Exception as e:
        print(f"Exception raised: {e}")



if __name__ == "__main__":
    get_statistics("TSM")
