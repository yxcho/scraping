import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import string
# pd.options.display.float_format = '{:.0f}'.format

FINVIZ_TABLE_ROW = 12
FINVIZ_TABLE_COL = 12


def convert_to_digits(numString: str) -> int:
    """
    Convert "570.68B" to 570680000000, "32.7m" to 32760000
    """
    try:
        numOfZeroes = {"T": 12, "B": 9, "M": 6, "K": 3}
        numInt = numString
        unit = numString[-1].upper()
        if unit in numOfZeroes:
            numString = numString[:-1]
            numFloat = float(numString)
            numInt = int(numFloat * pow(10, numOfZeroes[unit]))
        return numInt
    except Exception as e:
        print(f"Exception raised: {e}")


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
                value = convert_to_digits(features[row].contents[col+1].text)
                statistics[name] = value
                print(f"{name: <20} - {value: <20}")
        driver.close()
        return statistics

    except Exception as e:
        print(f"Exception raised: {e}")



if __name__ == "__main__":
    get_statistics("TSM")
