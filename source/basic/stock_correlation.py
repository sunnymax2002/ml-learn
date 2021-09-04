# https://github.com/NSEDownload/NSEDownload
from NSEDownload import stocks
from NSEDownload import indices
import pandas as pd
import matplotlib.pyplot as plt

# List of stock tickers t analyze
stock_list = ["SBIN", "HDFC", "IEX", "MCX"]

# Start and End dates
# TODO: change to download all available data
start_dt = "01-08-2019"
end_dt = "31-08-2021"

# First get data for 'Benchmark Index' - note Index name in call to get_data has space, but column in comb_df doesn't
benchmark_idx = "NIFTY 50"
comb_df = indices.get_data(indexName = benchmark_idx, start_date=start_dt, end_date=end_dt)
# Get only Close column and rename to index name
comb_df = comb_df[['Close']]
comb_df.columns = [benchmark_idx.replace(" ", "")]

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

# Display info and data colected
comb_df.info()
print(comb_df)

# Normalize before plotting
comb_df=(comb_df - comb_df.min()) / (comb_df.max() - comb_df.min())

comb_df.plot()
plt.show()