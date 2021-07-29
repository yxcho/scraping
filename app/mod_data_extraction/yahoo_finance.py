# import sys
# sys.path.append('../') 
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from enum import Enum
import pprint
pp = pprint.PrettyPrinter(indent=4)
pd.options.display.float_format = '{:.0f}'.format
# from general import common_functions

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



def get_analysis(ticker: str) -> dict:
    """
    Take note of the currency
    """
    try:
        is_link = f'https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(is_link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        features = soup.find_all('table', class_='W(100%)')
        if len(features) == 0:
            return None
            
        currency_declaration = soup.find_all('div', class_='Fz(xs)')[0].text
        statistics = {"statement currency": currency_declaration}

        footnotesCount = 7

        for feature in features:
            if len(feature.contents) == 2:
                name, value = feature.contents[0].text, convert_to_digits(feature.contents[1].text)
                if name[-1] in [str(num) for num in range(footnotesCount+1)]:
                    name = name[:-2]
                statistics[name.rstrip()] = value
                print(f"{name: <50} - {value: <20}")

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
        if len(features) == 0:
            return None
            
        currency_units_declaration = soup.find_all('span', class_='Fz(xs)')[0].text.split(". ")
        currency = currency_units_declaration[0]
        units = currency_units_declaration[1]
        headers = []
        temp_list = []
        final = []
        index = 1

        # create headers
        for header in features[0].contents:
            headers.append(header.text)
        # statement contents
        while index < len(features):
            for col in features[index].contents:
                temp_list.append(col.text)

            final.append(temp_list)
            # clear temp_list
            temp_list = []
            index += 1
        df = pd.DataFrame(final[:])
        df.columns = headers

        final_df = df.fillna('-')
        print(f"Statement currency: {currency}, units: {units}")
        return final_df

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
        if len(features) == 0:
            return None
            
        currency_declaration = soup.find_all('div', class_='C($gray)')[0].text
        statistics = {"statement currency": currency_declaration}

        footnotesCount = 7

        for feature in features:
            if len(feature.contents) == 2:
                name, value = feature.contents[0].text, convert_to_digits(feature.contents[1].text)
                if name[-1] in [str(num) for num in range(footnotesCount+1)]:
                    name = name[:-2]
                statistics[name.rstrip()] = value
                print(f"{name: <50} - {value: <20}")

        return pp.pprint(statistics)

    except Exception as e:
        print(f"Exception raised: {e}")






def get_stock_prices(ticker):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}')

    html = driver.execute_script("return document.body.innerHTML;")

    soup = BeautifulSoup(html, 'lxml')
    currency = soup.find_all("div", class_= "C($tertiaryColor) Fz(12px)")[0].text

    close_price = [entry.text for entry in soup.find_all(
        'span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]

    return currency, close_price[0] 


class FinancialStatement(Enum):
    IS = "Income Statement"
    BS = "Balance Sheet"
    CF = "Cash Flow"


if __name__ == "__main__":
    # print(get_financials("TSM", FinancialStatement.IS.value))
    # print(get_financials("TSM", FinancialStatement.BS.value))
    # print(get_financials("TSM", FinancialStatement.CF.value))
    # get_statistics("TSM")
    print(get_analysis("TSM"))

