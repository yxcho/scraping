# import sys
# sys.path.append('../')
from app.mod_general import common_functions
# from app.mod_general.static_variables import FinancialStatement
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
pd.options.display.float_format = '{:.0f}'.format
from enum import Enum

def get_analysis(ticker: str) -> dict:
    """
    Take note of the currency
    {'Earnings Estimate': {'No. of Analysts': '30', 'Avg. Estimate': '25.78', 'Low Estimate': '22.9', 'High Estimate': '30', 'Year Ago EPS': '26.29'}, 
    'Revenue Estimate': {'No. of Analysts': '30', 'Avg. Estimate': '68.12B', 'Low Estimate': '65.41B', 'High Estimate': '70.72B', 'Year Ago Sales': '55.31B', 'Sales Growth (year/est)': '23.20%'}, 
    'Earnings History': {'EPS Est.': '15.82', 'EPS Actual': '26.29', 'Difference': '10.47', 'Surprise %': '66.20%'}, 
    'EPS Trend': {'Current Estimate': '25.78', '7 Days Ago': '24.84', '30 Days Ago': '25.02', '60 Days Ago': '25.08', '90 Days Ago': '25.02'}, 
    'EPS Revisions': {'Up Last 7 Days': 'N/A', 'Up Last 30 Days': '21', 'Down Last 7 Days': 'N/A', 'Down Last 30 Days': 'N/A'}, 
    'Growth Estimates': {'Current Qtr.': '-1.90%', 'Next Qtr.': '2.60%', 'Current Year': '3.40%', 'Next Year': '16.60%', 'Next 5 Years (per annum)': '27.56%', 'Past 5 Years (per annum)': '14.93%'}, 'Symbol': {None: '26.13'}}
    """
    try:
        is_link = f'https://finance.yahoo.com/quote/{ticker}/analysis?p={ticker}'
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(is_link)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, "html.parser")

        features = soup.find_all('table', class_='W(100%)')
        if len(features) == 0:
            return None

        currency_declaration = soup.find_all('div', class_='Fz(xs)')[0].text
        statistics = {"statement currency": currency_declaration}

        footnotesCount = 7
        analysis_tables: dict[str, list] = {}

        for feature in features:
            table_name = feature.contents[0].contents[0].contents[0].text
            analysis_tables[table_name] = {}
            for table_row in feature.contents[1].contents:
                row_name = table_row.contents[0].string
                row_data = table_row.contents[1].string
                analysis_tables[table_name][row_name] = row_data

            # print(table_name, analysis_tables[table_name])
        driver.close()
        return analysis_tables

    except Exception as e:
        print(f"get_analysis exception raised: {e}")


def get_financials(ticker: str, statement_type: int) -> dict:
    """Return format:
        "data": {
        "Breakdown": {
            "0": "Operating Cash Flow",
            "1": "Investing Cash Flow",
            "2": "Financing Cash Flow",
            "3": "End Cash Position",
            "4": "Income Tax Paid Supplemental Data",
            "5": "Interest Paid Supplemental Data",
            "6": "Capital Expenditure",
            "7": "Issuance of Debt",
            "8": "Repayment of Debt",
            "9": "Repurchase of Capital Stock",
            "10": "Free Cash Flow"
        },
        "ttm": {
            "0": "8,789,500",
            "1": "-1,288,900",
            "2": "-7,774,300",
            "3": "2,982,000",
            "4": "-",
            "5": "-",
            "6": "-1,704,600",
            "7": "2,800",
            "8": "-3,188,100",
            "9": "-27,400",
            "10": "7,084,900"
        },
        "12/30/2020": {
            "0": "6,265,200",
            "1": "-1,545,800",
            "2": "-2,249,000",
            "3": "3,449,100",
            "4": "1,441,900",
            "5": "1,136,000",
            "6": "-1,640,800",
            "7": "5,543,000",
            "8": "-2,411,700",
            "9": "-907,800",
            "10": "4,624,400"
        },
        "12/30/2019": {
            "0": "8,122,100",
            "1": "-3,071,100",
            "2": "-4,994,800",
            "3": "898,500",
            "4": "1,589,700",
            "5": "1,066,500",
            "6": "-2,393,700",
            "7": "4,499,000",
            "8": "-2,061,900",
            "9": "-4,976,200",
            "10": "5,728,400"
        },
        "12/30/2018": {
            "0": "6,966,700",
            "1": "-2,455,100",
            "2": "-5,949,600",
            "3": "866,000",
            "4": "1,734,400",
            "5": "959,600",
            "6": "-2,741,700",
            "7": "3,794,500",
            "8": "-1,759,600",
            "9": "-5,207,700",
            "10": "4,225,000"
        },
        "12/30/2017": {
            "0": "5,551,200",
            "1": "562,000",
            "2": "-5,310,800",
            "3": "2,463,800",
            "4": "2,786,300",
            "5": "885,200",
            "6": "-1,853,700",
            "7": "4,727,500",
            "8": "-1,649,400",
            "9": "-4,685,700",
            "10": "3,697,500"
        },
        "Currency": "USD",
        "units": "All numbers in thousands"
    }
    """
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
        soup = BeautifulSoup(html, "html.parser")

        features = soup.find_all('div', class_='D(tbr)')
        if len(features) == 0:
            return None

        currency_units_declaration = soup.find_all(
            'span', class_='Fz(xs)')[0].text.split(". ")
        if len(currency_units_declaration) == 1 and "Currency" not in currency_units_declaration[0]:
            units = currency_units_declaration[0]
            currency = "USD"
        else:
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
        driver.close()
        result_json = final_df.to_json(orient="columns")
        parsed = json.loads(result_json)

        parsed["currency"] = currency
        parsed["units"] = units
        return parsed

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
        soup = BeautifulSoup(html, "html.parser")

        features = soup.find_all('tr', class_='Bxz(bb)')
        if len(features) == 0:
            return None

        currency_declaration = soup.find_all('div', class_='C($gray)')[0].text
        statistics = {"statement currency": currency_declaration}

        footnotesCount = 7

        for feature in features:
            if len(feature.contents) == 2:
                name, value = feature.contents[0].text, common_functions.convert_to_digits(
                    feature.contents[1].text)
                if name[-1] in [str(num) for num in range(footnotesCount+1)]:
                    name = name[:-2]
                statistics[name.rstrip()] = value
                print(f"{name: <50} - {value: <20}")
        driver.close()
        return statistics

    except Exception as e:
        print(f"Exception raised: {e}")


def get_stock_prices(ticker):

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}')

    html = driver.execute_script("return document.body.innerHTML;")

    soup = BeautifulSoup(html, "html.parser")
    currency = soup.find_all(
        "div", class_="C($tertiaryColor) Fz(12px)")[0].text

    close_price = [entry.text for entry in soup.find_all(
        'span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
    driver.close()

    return currency, close_price[0]




class FinancialStatement(Enum):
    IS = "Income Statement"
    BS = "Balance Sheet"
    CF = "Cash Flow"

if __name__ == "__main__":
    print(get_financials("MCD", FinancialStatement.IS.value))
    # print(get_financials("MCD", FinancialStatement.BS.value))
    # print(get_financials("MCD", FinancialStatement.CF.value))
    # get_statistics("TSM")
    # print(get_analysis("TSM"))
