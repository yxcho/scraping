from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from app.mod_general import common_functions


def get_ratios(url: str) -> dict:
    """go to investing.com, search for the stock, go to Financials -> Ratios, use the link
    eg: https://www.investing.com/equities/mcdonalds-ratios
    """
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        ratios = {}

        features = soup.find_all('tr', class_='child')
        if len(features) == 0:
            return None

        for row in features:
            if len(row.contents) == 7:
                name = row.contents[1].text
                company_ratio = common_functions.convert_to_digits(
                    row.contents[3].text)
                industry_ratio = common_functions.convert_to_digits(
                    row.contents[5].text)
                ratios[name] = [company_ratio, industry_ratio]
                # print(f"{name}: {company_ratio}, {industry_ratio}")
                print(f"{name: <50} - {company_ratio: <10} - {industry_ratio: <10}")
        driver.close()
        return ratios

    except Exception as e:
        print(f"Exception raised: {e}")


if __name__ == "__main__":
    url = "https://www.investing.com/equities/alibaba-ratios"
    get_ratios(url)
