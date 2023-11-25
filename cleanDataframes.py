import pandas as pd
import numpy as np
from datetime import datetime
import Keys
import os




def tickerToCompanyKey():
    os.environ['constituents_SAS'] = Keys.constituents_SAS_url
    constituentsDF = pd.read_csv(os.environ['constituents_SAS'])
    tickerToKey = dict(zip(constituentsDF["Symbol"], np.arange(1, len(constituentsDF) + 1).tolist()))
    return tickerToKey


def clean_constituents():
    os.environ['constituents_SAS'] = Keys.constituents_SAS_url
    constituentsDF = pd.read_csv(os.environ['constituents_SAS'])
    tickerToKey = tickerToCompanyKey()
    constituentsDF["CompanyKey"] = [tickerToKey[ticker] for ticker in constituentsDF["Symbol"]]
    constituentsDF.rename(columns={'Symbol': 'TickerSymbol', 'Name': 'CompanyName', 'Sector': 'SectorName'},
                          inplace=True)
    constituentsDF = constituentsDF[['CompanyKey', 'TickerSymbol', 'CompanyName', 'SectorName']]
    return constituentsDF


def clean_sectors():
    os.environ['sectors_SAS'] = Keys.sectors_SAS_url
    sectorsDF = pd.read_csv(os.environ['sectors_SAS'])
    sectorsDF["IndustryKey"] = np.arange(1, len(sectorsDF) + 1).tolist()
    sectorsDF.rename(columns={'SectorNumber': 'SectorCode', 'Sector': 'SectorName'}, inplace=True)
    sectorsDF = sectorsDF[["IndustryKey", "SectorName", "SectorCode"]]
    return sectorsDF


def clean_ratios():
    os.environ['ratios_SAS'] = Keys.ratios_SAS_url
    ratiosDF = pd.read_csv(os.environ['ratios_SAS'])
    ratiosDF.replace([np.inf, -np.inf], np.nan, inplace=True)
    ratiosDF.rename(columns={'Unnamed: 0': 'TickerSymbol', 'Unnamed: 1': 'RatioName',
                             '2023Q1': 'Q1', '2023Q2': 'Q2', '2023Q3': 'Q3'}, inplace=True)
    ratiosDF = ratiosDF.melt(id_vars=['TickerSymbol', 'RatioName'], value_vars=['Q1', 'Q2', 'Q3'])
    ratiosDF = ratiosDF.pivot(index=['TickerSymbol', 'variable'], columns='RatioName', values='value')
    ratiosDF.reset_index(inplace=True)
    quarterToDateInt = {'Q1': 20230331, 'Q2': 20230630, 'Q3': 20230930}
    ratiosDF["DateKey"] = [quarterToDateInt[quarter] for quarter in ratiosDF["variable"]]
    tickerToKey = tickerToCompanyKey()
    ratiosDF["CompanyKey"] = [tickerToKey[ticker] for ticker in ratiosDF["TickerSymbol"]]
    ratiosDF["FactKey"] = np.arange(1, len(ratiosDF) + 1).tolist()
    ratiosDF.rename(columns={'Asset Turnover Ratio': 'AssetTurnoverRatio',
                             'Operating Ratio': 'OperatingRatio',
                             'Current Ratio': 'CurrentRatio',
                             'Quick Ratio': 'QuickRatio',
                             'Cash Ratio': 'CashRatio',
                             'Working Capital': 'WorkingCapital',
                             'Operating Cash Flow Ratio': 'OperatingCashFlowRatio',
                             'Gross Margin': 'GrossMargin',
                             'Operating Margin': 'OperatingMargin',
                             'Net Profit Margin': 'NetProfitMargin',
                             'Interest Coverage Ratio': 'InterestCoverageRatio'
                             }, inplace=True)
    ratiosDF = ratiosDF[["FactKey", "DateKey", "CompanyKey", "AssetTurnoverRatio", "OperatingRatio",
                         "CurrentRatio", "QuickRatio", "CashRatio", "WorkingCapital",
                         "OperatingCashFlowRatio", "GrossMargin", "OperatingMargin",
                         "NetProfitMargin", "InterestCoverageRatio"]]
    subsetWithNANs = ratiosDF[ratiosDF.isna().any(axis=1) == True]
    originalSet = ratiosDF[~ratiosDF.FactKey.isin(subsetWithNANs.FactKey)]
    companiesWithNANs = subsetWithNANs.CompanyKey.unique().tolist()
    toInterpolate = ratiosDF[ratiosDF.CompanyKey.isin(companiesWithNANs)]
    columnsWithNANs = toInterpolate.columns.tolist()[3:]
    toInterpolate.reset_index(drop=True)

    interpolated = pd.DataFrame()
    for i in companiesWithNANs:
        df = toInterpolate.loc[toInterpolate["CompanyKey"] == i].reset_index(drop=True)
        for j in columnsWithNANs:
            if np.isnan(df[j]).any():
                if (~np.isnan(df[j][2])):
                    df.loc[:, j].bfill(inplace=True)
                else:
                    df.loc[:, j].fillna(value=df[j].mean(), inplace=True)
        interpolated = pd.concat([interpolated, df], axis=0)
    interpolated = interpolated.fillna(0)

    ratiosDF2 = pd.concat([originalSet, interpolated], axis=0)
    ratiosDF2.sort_values(by=['CompanyKey', 'DateKey'], ascending=[True, True], ignore_index=True, inplace=True)
    ratiosDF2.drop_duplicates(inplace=True)
    ratiosDF2['WorkingCapital'] = ratiosDF2['WorkingCapital'].apply(int)
    return ratiosDF2


def clean_stockprices():
    os.environ['stockperformance_SAS'] = Keys.stockperformance_SAS_url
    stockPerformanceDF = pd.read_csv(os.environ['stockperformance_SAS'])
    stockPerformanceDF['DateKey'] = stockPerformanceDF['Date'].apply(
        lambda x: datetime.strptime(x, '%Y-%m-%d').strftime("%Y%m%d"))
    stockPerformanceDF['DateKey'] = stockPerformanceDF['DateKey'].apply(int)
    stockPerformanceDF["FactKey"] = np.arange(1, len(stockPerformanceDF) + 1).tolist()
    tickerToKey = tickerToCompanyKey()
    stockPerformanceDF["CompanyKey"] = [tickerToKey[ticker] for ticker in stockPerformanceDF["Symbol"]]
    stockPerformanceDF.rename(columns={'Open': 'OpenPrice', 'Close': 'ClosePrice', 'Sector': 'SectorName'},
                              inplace=True)
    stockPerformanceDF = stockPerformanceDF[
        ['FactKey', 'DateKey', 'CompanyKey', 'OpenPrice', 'High', 'Low', 'ClosePrice', 'Volume']]
    stockPerformanceDF.round(2)
    return stockPerformanceDF


def date_table():
    start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2023-09-30", "%Y-%m-%d")
    date_list = pd.date_range(start_date, end_date, freq='D')
    date_list_iso = date_list.strftime("%Y-%m-%d")
    date_df = pd.DataFrame()
    date_df['DateISO'] = pd.to_datetime(date_list_iso)
    date_df["Year"] = date_df['DateISO'].dt.year.apply(int)
    date_df["YearName"] = date_df['DateISO'].dt.year.apply(str)
    date_df["MonthName"] = date_df['DateISO'].dt.month.apply(str).str.zfill(2)
    date_df["MonthNumber"] = date_df["MonthName"].apply(int)
    date_df["DayName"] = date_df['DateISO'].dt.month.apply(str).str.zfill(2)
    date_df["DayNumber"] = date_df["DayName"].apply(int)
    date_df["DateKey"] = (date_df["YearName"] + date_df["MonthName"] + date_df["DayName"]).apply(int)
    date_df['QuarterNumber'] = [3 if x >= 7 else 1 if x <= 3 else 2 for x in date_df['MonthNumber']]
    date_df['QuarterName'] = date_df['QuarterNumber'].apply(str)
    date_df = date_df[['DateKey', 'DateISO', 'Year', 'QuarterNumber', 'QuarterName',
                       'MonthNumber', 'MonthName', 'DayNumber', 'DayName']]
    return date_df
