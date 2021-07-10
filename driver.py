import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary
import string
pd.options.display.float_format = '{:.0f}'.format


def get_statistics(ticker: str) -> dict:
    try:
        is_link = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(is_link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        features = soup.find_all('tr', class_='Bxz(bb)')

        statistics = {}

        footnotesCount = 7

        for feature in features:
            if len(feature.contents) == 2:
                name, value = feature.contents[0].text, feature.contents[1].text
                if name[-1] in [str(num) for num in range(footnotesCount+1)]:
                    name = name[:-2]
                statistics[name.rstrip()] = value

        return statistics

    except Exception as e:
        print(f"Exception raised: {e}")


def stock_prices(ticker):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}')

    html = driver.execute_script("return document.body.innerHTML;")

    soup = BeautifulSoup(html, 'lxml')

    close_price = [entry.text for entry in soup.find_all(
        'span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    after_hours_price = [entry.text for entry in soup.find_all(
        'span', {'class': 'C($primaryColor) Fz(24px) Fw(b)'})]

    return(close_price, after_hours_price)


if __name__ == "__main__":
    # print(stock_prices("AAPL"))
    print(get_statistics("BABA"))
