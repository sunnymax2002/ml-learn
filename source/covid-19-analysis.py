#!/usr/bin/python
 
import pandas as pd
#from os import path
from datetime import datetime
import matplotlib.pyplot as plt
import helper_functions as hf

# Analyzes COVID-19 DF and extracts Top countries by Total Cases, their total deaths, % death to total cases and % cases to total population
def AggCasesDeaths(df):
    df_cases_and_deaths = df.groupby('countriesAndTerritories').agg(
        total_cases=pd.NamedAgg(column='cases', aggfunc='sum'),
        total_deaths=pd.NamedAgg(column='deaths', aggfunc='sum')
    )
    df_cases_and_deaths.info()
    df_cases_and_deaths['percent_death'] = (df_cases_and_deaths['total_deaths'] / df_cases_and_deaths['total_cases']) * 100
    #print(df_cases_and_deaths)

    # Calculate ww cases, deaths and % deaths
    total_ww_cases = df_cases_and_deaths['total_cases'].sum()
    total_ww_deaths = df_cases_and_deaths['total_deaths'].sum()
    avg_death_rate = total_ww_deaths / total_ww_cases * 100

    # Sort by total cases, highest first
    df_cases_and_deaths.sort_values(by='total_cases', inplace=True, ascending=False)

    num_toprows = 20
    df_top_cases_and_deaths = df_cases_and_deaths.loc[df_cases_and_deaths.iloc[0:num_toprows].index]
    #df_top_cases_and_deaths.info()

    # Get World Population Data
    pop_df = hf.GetWorldPopulationData()
    pop_df = pop_df[pop_df['Country Name'].isin(df_top_cases_and_deaths.index)]
    #print(pop_df)

    pop_df = pop_df.set_index('Country Name')
    #print(pop_df)

    #, fill_value=-1
    pop_df = pop_df.reindex(df_top_cases_and_deaths.index)
    #print(pop_df)

    # Calculate cases as milli-% of country population
    df_top_cases_and_deaths['cases_per_pop'] = df_top_cases_and_deaths['total_cases'] / pop_df['2018'] * 1000
    print(df_top_cases_and_deaths)

    return df_top_cases_and_deaths

# Plots aggregate dataset in bar charts
def PlotAggGraph(df_top_cases_and_deaths):
    plt.close('all')

    pd_plot = False

    if pd_plot:
        # Plotting with Pandas dataframe: https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html
        
        df_top_cases_and_deaths.iloc[:,[0,1]].plot.bar()
        #plt.show()

        df_top_cases_and_deaths.iloc[:,2].plot()
        #plt.show()

        df_top_cases_and_deaths.iloc[:,3].plot()
        plt.show()
    else:
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

        # Add labels above bars in total cases chart
        #AutoLabelBarChart(rc1, pc)

        fig.suptitle('COVID-19 Analysis of Top 20 Countries by Total Cases: ' + datetime.now().strftime("%d %B, %Y"), fontsize=20)
        plt.xticks(rotation=90)

        # TODO how to show as well as save to file?
        plt.show()
        gpath = hf.GetTempFileFullPath(datetime.now().strftime("%Y%m%d") + "-covid-19.png")
        #plt.savefig(gpath)

# Series Analysis
def TimeSeriesAnalysis(df, df_top_cases_and_deaths):
    # Visualize
    print()

# Get COVID-19 daily data into a DataFrame
df = hf.GetCovid19Data()

print("Processing DataFrame to find aggregates...")
df_top_cases_and_deaths = AggCasesDeaths(df)

print("Performing Time Series Analysis...")
TimeSeriesAnalysis(df, df_top_cases_and_deaths)

# Plot graphs
print("Plotting Graphs for Aggregates...")
PlotAggGraph(df_top_cases_and_deaths)