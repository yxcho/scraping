# import pandas as pd
from posixpath import islink
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import yfinance as yf
import pandas as pd
from enum import Enum
# from ..general import common_functions
import pprint
pp = pprint.PrettyPrinter(indent=4)
pd.options.display.float_format = '{:.0f}'.format


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
    """
    Take note of the currency
    """
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
                statistics[name.rstrip()] = convert_to_digits(
                    value)
                print(name, value)
        return pp.pprint(statistics)

    except Exception as e:
        print(f"Exception raised: {e}")


def get_financials(ticker: str, statement_type: int) -> dict:
    try:
        if statement_type == FinancialStatement.IS.value:
            url_type = "financials"
        elif statement_type == FinancialStatement.CF.value:
            url_type = "cash-flow"
        elif statement_type == FinancialStatement.BS.value:
            url_type = "balance-sheet"

        is_link = f"https://finance.yahoo.com/quote/{ticker}/{url_type}?p={ticker}"

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(is_link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        features = soup.find_all('div', class_='D(tbr)')

        headers = []
        temp_list = []
        final = []
        index = 0
        # create headers
        for item in features[0].find_all('div', class_='D(ib)'):
            headers.append(item.text)
        # statement contents
        while index <= len(features)-1:
            # filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                # each item adding to a temporary list
                temp_list.append(line.text)
            # temp_list added to final list
            final.append(temp_list)
            # clear temp_list
            temp_list = []
            index += 1
        df = pd.DataFrame(final[1:])
        df.columns = headers

        for column in headers[1:]:
            df[column] = common_functions.convert_to_numeric(df[column])
        final_df = df.fillna('-')
        return final_df

    except Exception as e:
        print(f"Exception raised: {e}")


def get_stock_prices(ticker):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}')

    html = driver.execute_script("return document.body.innerHTML;")

    soup = BeautifulSoup(html, 'lxml')

    close_price = [entry.text for entry in soup.find_all(
        'span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    # after_hours_price = [entry.text for entry in soup.find_all(
    #     'span', {'class': 'C($primaryColor) Fz(24px) Fw(b)'})]

    return close_price[0]  # , after_hours_price)


class FinancialStatement(Enum):
    IS = "Income Statement"
    BS = "Balance Sheet"
    CF = "Cash Flow"


if __name__ == "__main__":
    # print(get_financials("BABA", FinancialStatement.IS.value))
    # print(get_financials("BABA", FinancialStatement.BS.value))
    # print(get_financials("BABA", FinancialStatement.CF.value))
    print(get_statistics("BABA"))
    # print(get_stock_prices("BABA"))
