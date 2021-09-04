# https://github.com/NSEDownload/NSEDownload
from NSEDownload import stocks
import pandas as pd

stock_list = ["SBIN", "HDFC", "IEX", "MCX"]
#print(stock_list)

comb_df = pd.DataFrame()

for sym in stock_list:
	df = stocks.get_data(stockSymbol=sym, start_date = '30-12-2020', end_date = '2-2-2021') #full_data="Yes")
	df = df[['Close Price']]
	df.columns = [sym]
	#df.info()
	if(comb_df.empty):
		comb_df = df
	else:
		comb_df = pd.concat([comb_df, df], axis=1)

comb_df.info()
print(comb_df)