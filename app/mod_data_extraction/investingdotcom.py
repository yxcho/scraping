from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from general import common_functions


def convert_to_digits(numString: str) -> int:
    """
    Convert "570.68B" to 570680000000, "32.7m" to 32760000
    """
    try:
        numOfZeroes = {"T": 12,"B": 9, "M": 6, "K": 3}
        numInt = numString
        unit = numString[-1].upper()
        if unit in numOfZeroes:
            numString = numString[:-1]
            numFloat = float(numString)
            numInt = int(numFloat * pow(10, numOfZeroes[unit]))
        return numInt
    except Exception as e:
        print(f"Exception raised: {e}")

def get_ratios(url):
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
                company_ratio = convert_to_digits(row.contents[3].text)
                industry_ratio = convert_to_digits(row.contents[5].text)
                ratios[name] = [company_ratio, industry_ratio]
                # print(f"{name}: {company_ratio}, {industry_ratio}")
                print(f"{name: <50} - {company_ratio: <10} - {industry_ratio: <10}")
        return ratios

    except Exception as e:
        print(f"Exception raised: {e}")


if __name__ == "__main__":
    url = "https://www.investing.com/equities/alibaba-ratios"
    get_ratios(url)
