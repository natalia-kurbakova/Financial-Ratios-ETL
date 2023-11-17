import yfinance as yf
import pandas as pd
from financetoolkit import Toolkit
import Keys
import os
import webscrape

base_path = os.getcwd()
file_path = os.path.join(base_path, r'csvFiles')
if not os.path.exists(file_path):
   os.makedirs(f"{file_path}", exist_ok=True)

constituents = webscrape.constituentsToDF()


def StockPreformanceToDF():
    stockPerformance = pd.DataFrame()
    for symbol in constituents.Symbol:
        ticker = yf.Ticker(symbol)
        data = ticker.history(start="2023-01-01", end="2023-09-30", interval="1d")
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date']).dt.date
        data.insert(1, "Symbol", symbol)
        stockPerformance = pd.concat([stockPerformance, data])
    return stockPerformance

def StockPreformanceToCSV():
    df = StockPreformanceToDF()
    if not os.path.exists(f"{file_path}/stockPerformance.csv"):
        return df.to_csv(f"{file_path}/stockPerformance.csv", index=False)


def RatiosToDF():
    os.environ['FMP'] = Keys.FINANCIAL_MODELING_PREP_KEY
    custom_ratios = {
        'Asset Turnover Ratio': 'Asset Turnover Ratio',
        'Operating Ratio': 'Operating Ratio',
        'Current Ratio': 'Current Ratio',
        'Quick Ratio': 'Quick Ratio',
        'Cash Ratio': 'Cash Ratio',
        'Working Capital': 'Working Capital',
        'Operating Cash Flow Ratio': 'Operating Cash Flow Ratio',
        'Gross Margin': 'Gross Margin',
        'Operating Margin': 'Operating Margin',
        'Net Profit Margin': 'Net Profit Margin',
        'Interest Coverage Ratio': 'Interest Coverage Ratio',
        'Net Current Asset Value': 'Net Current Asset Value'
    }
    companies = Toolkit(
        tickers=list(constituents.Symbol),
        api_key=os.environ['FMP'],
        start_date="2022-12-01",
        custom_ratios=custom_ratios,
        quarterly=True
    )

    custom_ratios = companies.ratios.collect_custom_ratios()
    return custom_ratios




def RatiosToCSV():
    df = RatiosToDF()
    df.drop(columns=['2022Q4', '2023Q4'], axis=1, inplace=True)
    if not os.path.exists(f"{file_path}/ratios.csv"):
        return df.to_csv(f"{file_path}/ratios.csv", index=True)

def main():
    print("[Extract] Downloading S&P100 stock performance to csvFiles folder")
    StockPreformanceToCSV()
    print("[Extract] Downloading financial ratios to csvFiles folder")
    RatiosToCSV()