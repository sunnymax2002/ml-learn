import requests
from os import path
import pandas as pd
import tempfile
from datetime import datetime

def GetFileFromUrl(url, fpath):
    if(not path.exists(fpath)):
        print("[HF] Downloading dataset to local file: " + fpath)
        # Download from URL into a file-like object
        uf = requests.get(url)

        # Write to disk file
        f = open(fpath, 'wb')
        f.write(uf.content)
        f.close()

def GetTempFileFullPath(fname):
    return path.join(tempfile.gettempdir(), fname)


def GetCovid19Data():
    # Worldwide daily COVID-19 numbers by country: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863
    url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
    print("[HF] Obtaining Data from " + url)
    # Filename with today's date
    fpath = path.join(tempfile.gettempdir(), datetime.now().strftime("%Y%m%d") + "-covid-19.xlsx")
    GetFileFromUrl(url, fpath)

    # Read XLSX file into Pandas DataFrame
    print("[HF] Reading local file to load DataFrame...")
    return pd.read_excel(fpath)

def GetWorldPopulationData():
    # Obtain population data
    url = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=excel"
    print("[HF] Obtaining Data from " + url)
    fpath = "D:\Learning\My Code\git_repos\ml-learn\datasets\API_SP.POP.TOTL_DS2_en_excel_v2_935990.xls"
    GetFileFromUrl(url, fpath)

    print("[HF] Reading local file to load DataFrame...")
    # Ignore first 3 rows in XLS sheet0
    # TODO find the latest year column instead of hard-coding to '2018'
    print("[HF] Population Data from Year 2018...")
    return pd.read_excel(fpath, header=3, usecols=['Country Name', '2018'])

# Usage Example:
#   rc1 = pc.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.total_cases)
#   AutolabelBarChart(rc1, pc)
def AutolabelBarChart(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')