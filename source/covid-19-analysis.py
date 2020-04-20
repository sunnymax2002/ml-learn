import pandas as pd
from os import path
import tempfile
from datetime import datetime
import requests
import matplotlib.pyplot as plt

# Filename with today's date
tday = datetime.now()
tday = tday.strftime("%Y%m%d") + "-covid-19.xlsx"
fpath = path.join(tempfile.gettempdir(), tday)

if(not path.exists(fpath)):
    print("Downloading dataset to local file...")
    # Fetch dataset using URL
    # Worldwide daily numbers by country: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863
    url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
    # Download from URL into a file-like object
    uf = requests.get(url)

    # Write to disk file
    f = open(fpath, 'wb')
    f.write(uf.content)
    f.close()

# Read XLSX file into Pandas DataFrame
print("Reading local file to load DataFrame...")
df = pd.read_excel(fpath)

#print("\n\nCOVID-19 DataFrame Info:")
#df.info()

# Sort by total # of cases
#print("\n\nTop Countries in terms of Total Cases:")
#df_cases = df.groupby('countriesAndTerritories').cases.agg([sum])
#df_cases.sort_values(by='sum', inplace=True, ascending=False)
#print(df_cases)

#print("\n\nCOVID-19 Total Cases and Deaths, by Country:")
# Group the table by countries, and calculate total cases and total deaths

#df_cases_and_deaths = df.groupby('countriesAndTerritories').agg({
#    'cases':['sum'],
#    'deaths':['sum']
#})

print("Processing DataFrame...")

df_cases_and_deaths = df.groupby('countriesAndTerritories').agg(
    total_cases=pd.NamedAgg(column='cases', aggfunc='sum'),
    total_deaths=pd.NamedAgg(column='deaths', aggfunc='sum')
)
df_cases_and_deaths.info()
df_cases_and_deaths['percent_death'] = (df_cases_and_deaths['total_deaths'] / df_cases_and_deaths['total_cases']) * 100
print(df_cases_and_deaths)

# Calculate ww cases, deaths and % deaths
total_ww_cases = df_cases_and_deaths['total_cases'].sum()
total_ww_deaths = df_cases_and_deaths['total_deaths'].sum()
avg_death_rate = total_ww_deaths / total_ww_cases * 100

# Sort by total cases, highest first
df_cases_and_deaths.sort_values(by='total_cases', inplace=True, ascending=False)

num_toprows = 20
df_top_cases_and_deaths = df_cases_and_deaths.loc[df_cases_and_deaths.iloc[0:num_toprows].index]
df_top_cases_and_deaths.info()

# Plot graphs
print("Plotting Graphs...")
plt.close('all')

fig, (pc, pd, pdr) = plt.subplots(nrows=3, sharex=True)
pc.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.total_cases)
pc.set_ylabel('Total Cases')

pd.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.total_deaths, color='grey')
pd.set_ylabel('Total Deaths')

pdr.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.percent_death, color='red')
pdr.set_ylabel('Percentage Deaths')

fig.suptitle('COVID-19 Analysis of Top 20 Countries by Total Cases: ' + datetime.now().strftime("%d %B, %Y"), fontsize=20)
plt.xticks(rotation=90)

#ax2 = ax.twinx()
#df_top_cases_and_deaths.plot()
#df_top_cases_and_deaths.plot(y='percent_death', kind='bar')

plt.show()

print(df_top50_cases_and_deaths)