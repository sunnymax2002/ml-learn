#!/usr/bin/python
 
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import helper_functions as hf
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import math

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

    # TODO: COVID-19 df already has Population Data, comment this out and use it instead
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

# Function estimator for virus outbreak
#   k - growth factor
#   
def Covid19Estimator(x, x0, k0, P):
    # Full curve will reducing part
#    y = P * ( (1 / (1 + np.exp( -k*(x-x0) ) ) ) + (1 / (1 + np.exp( -k*(x1-x) ) ) ) )

    # Partial curve only with increase
    y = P * ( (1 / (1 + np.exp( -k0*(x-x0) ) ) ) )

    return y

def Covid19EstimatorFull(x, x0, k0, P, x1):
    # Full curve will reducing part
    y = P * ( (1 / (1 + np.exp( -k0*(x-x0) ) ) ) + (1 / (1 + np.exp( -k0*(x1-x) ) ) ) - 1 )

    return y

def TestEstimator():
    x = np.linspace(0, 1000, 1000)
    #print(x)

    y = Covid19Estimator(x, 300, 800, 0.03, 1000)

    #print(y)
    plt.plot(y)
    plt.show()
    print(y)

# Series Analysis
def TimeSeriesAnalysis(df, df_top_cases_and_deaths):
    # Visualize the time series
    fig, ax = plt.subplots(nrows=5, ncols=4, sharex=True)

    # Extract time series for the top country
    for countryIndex in range(0, 20):
        dfts = df.loc[df['countriesAndTerritories'].eq(df_top_cases_and_deaths.index[countryIndex]), 
            ['dateRep', 'cases', 'deaths']].sort_values(by='dateRep').set_index('dateRep')
        #print(dfts)

        # Obtain cumulative sums for cases and deaths
        dftscum = dfts.cumsum()
        #dfts.info()
        #print(dftscum)

        #dftscum.plot() #x='dateRep', y='cases')
        #plt.show()

        # Curve fitting
        actdays = len(dftscum)
        estdays = 3 * actdays
        x = list(range(0, actdays))
        popt, pcov = curve_fit(Covid19Estimator, x, dftscum.cases)
        print(popt)

        x0 = popt[0]

        # Adjust 'gain'
        gain = 1
        k0 = popt[1] * gain
        P = popt[2]

        # Extrapolate
        x = list(range(0, estdays))
        y = Covid19Estimator(x, x0, k0, P)
        
        y0 = dftscum.cases.tolist()
        y1 = [0] * (estdays - len(dftscum.cases))
        y0 += y1

        # Find x1 for Covid19EstimatorFull
        #   x1 > x0
        #   xP for which y = ymax
        #   x1 - xP nearly equal to xP - x0
        #   Assume x1-max = 10000
        # Find near peak [y]
        ynp = 0.99 * P
        for i in range(int(x0), len(y)):
            yi = y[i]
            if yi >= ynp:
                break
        
        # x1 is at same distance from x-yp as x0
        x1 = i + (i - x0)

        # Calculate decreasing values
        yf = Covid19EstimatorFull(x, x0, k0, P, x1)
        
        r = math.floor(countryIndex / 4)
        c = countryIndex % 4

        ax[r, c].scatter(x, y0, color='green', marker='.')
        #plt.plot(x, y, color='red')

        # Blue dotted estimated plot
        ax[r, c].plot(x, yf, 'b:')

        #plt.plot(y)
        #a1.plot(y)
        #plt.plot(dftscum.cases, color='red')

    plt.show()

#TestEstimator()

# Get COVID-19 daily data into a DataFrame
df = hf.GetCovid19Data()

print("Processing DataFrame to find aggregates...")
df_top_cases_and_deaths = AggCasesDeaths(df)

# Plot graphs
print("Plotting Graphs for Aggregates...")
PlotAggGraph(df_top_cases_and_deaths)

print("Performing Time Series Analysis...")
TimeSeriesAnalysis(df, df_top_cases_and_deaths)