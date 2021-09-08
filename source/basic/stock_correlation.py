# https://github.com/NSEDownload/NSEDownload
from NSEDownload import stocks
from NSEDownload import indices
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np

# List of stock tickers t analyze
stock_list = ["SBIN", "HDFC", "IEX", "MCX"]

# Start and End dates
# TODO: change to download all available data
start_dt = "01-01-2020"
end_dt = "31-08-2021"

# First get data for 'Benchmark Index' - note Index name in call to get_data has space, but column in comb_df doesn't
benchmark_idx = "NIFTY 50"
bidx_col = benchmark_idx.replace(" ", "")

# Check if pickled dataframe available
pkl_file = "./stock_data.pkl"

if os.path.exists(pkl_file):
    comb_df = pd.read_pickle(pkl_file)
else:
    comb_df = indices.get_data(indexName = benchmark_idx, start_date=start_dt, end_date=end_dt)
    # Get only Close column and rename to index name
    comb_df = comb_df[['Close']]
    comb_df.columns = [bidx_col]

    # For each ticker...
    for sym in stock_list:
        # Get stock data from NSE website and select only the 'Close Price'
        df = stocks.get_data(stockSymbol=sym, start_date=start_dt, end_date=end_dt) #full_data="Yes")
        df = df[['Close Price']]

        # Rename Close Price column to match ticker name
        df.columns = [sym]

        # Concatenate new data into combined dataframe
        if(comb_df.empty):
            comb_df = df
        else:
            comb_df = pd.concat([comb_df, df], axis=1)

    # Change index dtype to DateTime and sort on index
    comb_df.index = pd.to_datetime(df.index)
    comb_df.sort_index(inplace=True)

    # Pickle the downloaded data for next use
    comb_df.to_pickle(pkl_file)
    print("Picked the downloaded stock data")

# Display info and data colected
comb_df.info()
print(comb_df)

# Find monthly min max for index: Groupby 'month' on DateTimeIndex,
#       and then find indices of min/max,
#       and select those rows into a new dataframe,
#       and remove 'stock' columns,
#       and finally sort again on date index
minmax_df = pd.concat([comb_df.loc[comb_df.groupby(pd.Grouper(freq="M"))[bidx_col].idxmin()],
    comb_df.loc[comb_df.groupby(pd.Grouper(freq="M"))[bidx_col].idxmax()]], axis=0)
minmax_df.sort_index(inplace=True)
minmax_df.info()

#minmax_df.plot()
#plt.show()

# Use linear regression to find trned in index price movement
y = comb_df[bidx_col].values
x = np.arange(y.shape[0])

slope, intercept, r_val, p_val, std_err = stats.linregress(x, y)
print(slope, intercept, r_val, p_val, std_err)

exit()

# Normalize before plotting
comb_df=(comb_df - comb_df.min()) / (comb_df.max() - comb_df.min())

comb_df.plot()
plt.show()