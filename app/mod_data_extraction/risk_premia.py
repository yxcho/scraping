"""
To get the risk free rate (Rf) and implied market risk premium (IMRP) of a country
ICOC = Risk free rate + Implied market risk premium
http://www.market-risk-premia.com/us/#tabs-3

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time, requests
from app.mod_general import common_functions

def get_icoc(country):
    try:
        # url = f"http://www.market-risk-premia.com/{country.lower()}/#tabs-3"
        url = f"http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html"
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.get(url)

        # time.sleep(3)
        # page = driver.page_source
        # driver.quit()
        # soup = BeautifulSoup(page, 'html.parser')
        # container = soup.find_all('div', attrs={
        #     'class':'js-event-list-tournament-events'})

        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for row in soup.find('table').find_all('tr'):
            for col in row.contents:
                print(col.text)
            # print(row.contents)
            # print(' '.join([x.text for x in row.find_all('td')]))
            # Or just use '[x.text for x in row.find_all('td')]' in your data frame.


        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, "html.parser")


        ratios = {}

        features = soup.find_all('tr', class_='child')
        features = soup.find_all('table', {"class": "display"})

        for row in features:
            if len(row.contents) == 7:
                name = row.contents[1].text
                company_ratio = common_functions.convert_to_digits(row.contents[3].text)
                industry_ratio = common_functions.convert_to_digits(row.contents[5].text)
                ratios[name] = [company_ratio, industry_ratio]
                # print(f"{name}: {company_ratio}, {industry_ratio}")
                print(f"{name: <50} - {company_ratio: <10} - {industry_ratio: <10}")
        return ratios

    except Exception as e:
        print(f"Exception raised: {e}")
# market-return-analysis_market-return-analysis-icoc-risk-free-rate-implied-market-risk-premium
# even group-item group-item-market-return-analysis subgroup-item group-item-market-return-analysis_market-return-analysis-icoc-risk-free-rate-implied-market-risk-premium
if __name__ == "__main__":
    get_icoc("US")



