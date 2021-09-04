# Covid-19 vaccination effectiveness

import requests
from os import path
import pandas as pd
import tempfile
from datetime import datetime

fpath = path.join(tempfile.gettempdir(), datetime.now().strftime("%Y%m%d") + "-covid-19-vax.xlsx")
uf = requests.get("https://covid.ourworldindata.org/data/owid-covid-data.csv")

f = open(fpath, 'wb')
f.write(uf.content)
f.close()

df = pd.read_csv(fpath)
df.info()