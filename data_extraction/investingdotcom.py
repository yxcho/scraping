from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def get_ratios(url):
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')

        ratios = {}

        features = soup.find_all('tr', class_='child')

        for row in features:
            if len(row.contents) == 7:
                name = row.contents[1].text
                company_ratio = row.contents[3].text
                industry_ratio = row.contents[5].text
                ratios[name] = [company_ratio, industry_ratio]
                print(f"{name}: {company_ratio}, {industry_ratio}")

        return ratios

    except Exception as e:
        print(f"Exception raised: {e}")



if __name__ == "__main__":
    url = "https://www.investing.com/equities/alibaba-ratios"
    print(get_ratios(url))