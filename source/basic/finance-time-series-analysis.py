import matplotlib.pyplot as plt
import helper_functions as hf
from pandas.plotting import autocorrelation_plot

#import quandl
# My QUANDL API_KEY:
#quandl.ApiConfig.api_key = '49thVPqqr_9BPMHXsRfS'
#mydata = quandl.get('FSE/EON_X')

df = hf.GetIndiaNifty500HistData()
df.
df.info()
print(df)

fig, ax = plt.subplots(nrows=2)

#x=df.Date, 
df.Price.plot(ax=ax[0])
#plt.plot(df.Date, df.Price)
autocorrelation_plot(df.Price, ax=ax[1])
plt.show()

