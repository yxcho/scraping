import requests
from bs4 import BeautifulSoup


def scrape_jobs(location=None):
    """Scrapes Developer job postings from Monster, optionally by location.
    :param location: Where the job is located
    :type location: str
    :return: all job postings from first page that match the search results
    :rtype: BeautifulSoup object
    """
    # URL = (f"https://www.morningstar.com/stocks/xnas/aapl/quote")
    URL = ("https://www.reuters.com/companies/AAPL.OQ")
    # URL = ("https://finviz.com/quote.ashx?t=AAPL")

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    return soup


if __name__ == "__main__":
    results = scrape_jobs()
    print(results)