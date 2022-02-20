from app.mod_data_extraction import yahoo_finance
from app.mod_data_extraction.API import alpha_vantage, rapidAPI
from app.mod_formulae.dcf_20_year import DiscountRateCalculator, DCFCalculator, IVCalculator
from app.mod_general import common_functions

def calculate_iv(ticker: str):
    """
    1. extract data
    2. validate data
    3. calculate intrinsic price
    4. present data


    rfrate, market_risk_premium, country

    Alpha vantage
    shares_outstanding - balance_sheet["annualReports"][0]["commonStockSharesOutstanding"]
    cash_flow - cash_flow["annualReports"][0]["operatingCashflow"] - ["annualReports"][0]["capitalExpenditures"]
    cash_and_inv - balance_sheet["annualReports"][0]["cashAndShortTermInvestments"]
    net income common stockholder (current) - income_statement["annualReports"][0]["netIncome"]

    rapidAPI
    total_debt - ["financialData"]["totalDebt"]["raw"]
    company_beta - ["defaultKeyStatistics"]["beta"]["raw"]
    stock currency - ["price"]["currency"]
    statement currency - ["financialData"]["financialCurrency"]
    currrent price - ["financialData"]["currentPrice"]["raw"]

    Yahoo finance
    one_to_five_y_growth_rate, six_to_ten_y_growth_rate, eleven_to_twenty_y_growth_rate
     - yf_analysis["Growth Estimates"]["Next 5 Years (per annum)"]
    """
    try:
        yf_analysis = yahoo_finance.get_analysis(ticker)
        av_income_statement = alpha_vantage.get_income_statement(ticker)
        av_cash_flow = alpha_vantage.get_cash_flow(ticker)
        av_balance_sheet = alpha_vantage.get_balance_sheet(ticker)
        rapidapi_stats = rapidAPI.get_statistics(ticker)

        shares_outstanding = int(av_balance_sheet["annualReports"][0]["commonStockSharesOutstanding"])
        cash_flow = int(av_cash_flow["annualReports"][0]["operatingCashflow"]) - int(av_cash_flow["annualReports"][0]["capitalExpenditures"])
        cash_and_inv = int(av_balance_sheet["annualReports"][0]["cashAndShortTermInvestments"])
        net_income = int(av_income_statement["annualReports"][0]["netIncome"])

        one_to_five_y_growth_rate = yf_analysis["Growth Estimates"]["Next 5 Years (per annum)"]
        one_to_five_y_growth_rate = common_functions.convert_percentage_to_float(one_to_five_y_growth_rate)

        total_debt = rapidapi_stats["financialData"]["totalDebt"]["raw"]
        company_beta = rapidapi_stats["defaultKeyStatistics"]["beta"]["raw"]
        stock_currency = rapidapi_stats["price"]["currency"]
        statement_currency = rapidapi_stats["financialData"]["financialCurrency"]
        currrent_price = rapidapi_stats["financialData"]["currentPrice"]["raw"]

        six_to_ten_y_growth_rate = one_to_five_y_growth_rate/2  
        eleven_to_twenty_y_growth_rate = 0.0418
        risk_free_rate = 0.016
        market_risk_premium = 0.0428

        print(f"Cash flow: {cash_flow}")
        print(f"total debt: {total_debt}")
        print(f"Cash and short term investments: {cash_and_inv}")
        print(f"one to five year growth rate: {one_to_five_y_growth_rate}")
        print(f"Shares outstanding: {shares_outstanding}")
        print(f"net income: {net_income}")
        print(f"Company beta: {company_beta}")
        print(f"Stock currency: {stock_currency}")
        print(f"statement currency: {statement_currency}")
        print(f"current price: {currrent_price}")


        discount_rate = DiscountRateCalculator(risk_free_rate, company_beta, market_risk_premium).get_company_discount_rate()
        pv = DCFCalculator(cash_flow, one_to_five_y_growth_rate, six_to_ten_y_growth_rate, eleven_to_twenty_y_growth_rate, discount_rate).get_pv_of_20y_fcf()
        final_iv = IVCalculator(shares_outstanding, total_debt, cash_and_inv, pv).get_final_iv()
        return final_iv

    except Exception as e:
        print(f"calculate_iv raised exception: {e}")