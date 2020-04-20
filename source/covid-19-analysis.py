#!/usr/bin/python
 
import pandas as pd
from os import path
import tempfile
from datetime import datetime
import matplotlib.pyplot as plt
import helper_functions as hf

# Worldwide daily COVID-19 numbers by country: https://data.europa.eu/euodp/en/data/dataset/covid-19-coronavirus-data/resource/55e8f966-d5c8-438e-85bc-c7a5a26f4863
url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx'
# Filename with today's date
fpath = path.join(tempfile.gettempdir(), datetime.now().strftime("%Y%m%d") + "-covid-19.xlsx")
hf.GetFileFromUrl(url, fpath)

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

# Obtain population data
url = "http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=excel"
fpath = "D:\Learning\My Code\git_repos\ml-learn\datasets\API_SP.POP.TOTL_DS2_en_excel_v2_935990.xls"
hf.GetFileFromUrl(url, fpath)

pop_df = pd.read_excel(fpath, header=3, usecols=['Country Name', '2018'])
pop_df = pop_df[pop_df['Country Name'].isin(df_top_cases_and_deaths.index)]
print(pop_df)

pop_df = pop_df.set_index('Country Name')
print(pop_df)

#, fill_value=-1
pop_df = pop_df.reindex(df_top_cases_and_deaths.index)
print(pop_df)

# Calculate cases as milli-% of country population
df_top_cases_and_deaths['cases_per_pop'] = df_top_cases_and_deaths['total_cases'] / pop_df['2018'] * 1000
print(df_top_cases_and_deaths)

# Plot graphs
print("Plotting Graphs...")
plt.close('all')

fig, (pc, pd, pdr, pcp) = plt.subplots(nrows=4, sharex=True)
rc1 = pc.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.total_cases)
pc.set_ylabel('Total Cases')

pd.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.total_deaths, color='grey')
pd.set_ylabel('Total Deaths')

# Note: To plot two series on same chart with 2 y-axis, pdr = pd.twinx() ...
pdr.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.percent_death, color='red')
pdr.set_ylabel('Percentage Deaths')

pcp.bar(df_top_cases_and_deaths.index, df_top_cases_and_deaths.cases_per_pop, color='green')
pcp.set_ylabel('Cases as Milli-% Population')

def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Add labels above bars in total cases chart
#autolabel(rc1, pc)

fig.suptitle('COVID-19 Analysis of Top 20 Countries by Total Cases: ' + datetime.now().strftime("%d %B, %Y"), fontsize=20)
plt.xticks(rotation=90)

#ax2 = ax.twinx()
#df_top_cases_and_deaths.plot()
#df_top_cases_and_deaths.plot(y='percent_death', kind='bar')

#plt.show()

gpath = path.join(tempfile.gettempdir(), datetime.now().strftime("%Y%m%d") + "-covid-19.png")
plt.savefig(gpath)