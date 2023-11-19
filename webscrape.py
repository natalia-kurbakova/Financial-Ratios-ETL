# !pip install -r requirements.txt    <- install modules on your local machine

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os


base_path = os.getcwd()
file_path = os.path.join(base_path, r'csvFiles')
if not os.path.exists(file_path):
   os.makedirs(f"{file_path}", exist_ok=True)

def constituentsToDF():
    # scraping the table from the right website
    url = 'https://en.wikipedia.org/wiki/S%26P_100#Components'
    file = requests.get(url)
    mysoup = BeautifulSoup(file.content, 'html.parser')
    table = mysoup.find('table', class_="wikitable sortable")
    # creating a list for the rows of the table and modifying table data text so it is easier to work with
    for child in table:
        rows = []
        for td in child:
            try:
                rows.append(td.text.split("\n"))
            except:
                continue
    # from each row removing the element that contains an empty value
    for row in rows:
        for element in row:
            if element == '':
                row.remove(element)

    rows = rows[::2]  # do not touch
    # convert the list into dataframe row by adding columns
    constituents = pd.DataFrame(rows[1:], columns=rows[0])
    constituents.replace("BRK.B", "BRK-B", inplace=True)    #yahoo finance only supports with dash
    return constituents

def constituentsToCSV():
    df = constituentsToDF()
    if not os.path.exists(f"{file_path}/constituents.csv"):
        return df.to_csv(f"{file_path}/constituents.csv", index=False)


def gicsToDF():  #GICS stands for global industry classification standard
    # scraping the table from the right website
    url2 = 'https://en.wikipedia.org/wiki/Global_Industry_Classification_Standard'
    file2 = requests.get(url2)
    mysoup2 = BeautifulSoup(file2.content, 'html.parser')
    table2 = mysoup2.find('table', class_="wikitable")
    # creating a list for the rows of the table and modifying table data text so it is easier to work with
    for child in table2:
        rows2 = []
        for td in child:
            try:
                rows2.append(td.text.split("\n"))
            except:
                continue
    rows2 = rows2[::2]
    for row in rows2:
        for element in row:
            if element == '':
                row.remove(element)
    index = []
    sector = []

    for row in rows2[1:]:
        if len(row[0]) == 2:
            index.append(row[0])
            sector.append(row[1])
    gicsDf = pd.DataFrame({"SectorNumber": index, "Sector": sector})
    return gicsDf

def gicsToCSV():
    df = gicsToDF()
    if not os.path.exists(f"{file_path}/sector.csv"):
        return df.to_csv(f"{file_path}/sector.csv", index=False)


def main():
    print("[Extract] Downloading S&P100 constituents file to csvFiles folder")
    constituentsToCSV()
    print("[Extract] Downloading GICS (company sector) table to csvFiles folder")
    gicsToCSV()