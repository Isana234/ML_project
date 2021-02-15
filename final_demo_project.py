# -*- coding: utf-8 -*-
"""Final_Demo_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m8bKO-RDrskvNQkKX2zntMhaHztN3sh3

# ARIMA and Seasonal ARIMA


## Autoregressive Integrated Moving Averages
* Data Preprocessing
* Visualize the Time Series Data
* Make the time series data stationary
* Plot the Correlation and AutoCorrelation Charts
* Construct the ARIMA Model or Seasonal ARIMA based on the data
* Use the model to make predictions

## Data Preprocessing
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
# %matplotlib inline 
#plot outputs appear and be stored within the notebook
def hello(file):
	df=pd.read_csv("{}".format(file),sep=",")

	df.head()

	df.tail()

	## Cleaning up the data
	df.columns=["Month","Sales"]
	df.head()
	df=df.dropna()
	print(df)



	df.tail()


	
	import plotly.graph_objects as go
	fig = go.Figure(data=[go.Table(
	    header=dict(values=list(df.columns),
	                fill_color='paleturquoise',
	                align='left'),
	    cells=dict(values=[df.Month,df.Sales],
	               fill_color='lavender',
	               align='left'))
	])

	fig.show()
	# Convert Month into Datetime
	df['Month']=pd.to_datetime(df['Month'])

	df.head()
	df.set_index('Month',inplace=True)

	df.head()

	df.describe()

	"""##Visualizing the Data"""

	#df.plot()

	"""**Check for stationarity** """

	#!pip install pandas.plotting
	from pandas.plotting import autocorrelation_plot
	#autocorrelation_plot(df['Sales'])
	#plt.show()

	### Testing For Stationarity

	from statsmodels.tsa.stattools import adfuller

	test_result=adfuller(df['Sales'])

	#Ho: It is non stationary (Null hypothesis)
	#H1: It is stationary

	def adfuller_test(sales):
	    result=adfuller(sales)
	    print('ADF Statistic: %f' % result[0])
	    print('p-value: %f' % result[1])
	    print('Critical Values:')
	    for key, value in result[4].items():
	        print('\t%s: %.3f' % (key, value))

	    if result[0] < result[4]["5%"]:
	        print ("Reject Ho - Time Series is Stationary")
	    else:
	        print ("Failed to Reject Ho - Time Series is Non-Stationary")

	adfuller_test(df['Sales'])

	"""## Differencing"""

	df['Sales First Difference'] = df['Sales'] - df['Sales'].shift(1)

	df['Sales'].shift(1)

	df['Seasonal First Difference']=df['Sales']-df['Sales'].shift(12)

	df.head(14)

	## Again test dickey fuller test
	adfuller_test(df['Seasonal First Difference'].dropna())

	#df['Seasonal First Difference'].plot()

	"""### Autocorrelation and Partial Autocorrelation

	* Identification of an AR model is often best done with the PACF.

	* Identification of an MA model is often best done with the ACF rather than the PACF.
	    
	    p,d,q
	    p AR model lags
	    d differencing
	    q MA lags
	"""

	from statsmodels.graphics.tsaplots import plot_acf,plot_pacf

	import statsmodels as sm
	#fig = plt.figure(figsize=(12,8))
	#ax1 = fig.add_subplot(211)
	#fig = sm.graphics.tsaplots.plot_acf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax1)
	#ax2 = fig.add_subplot(212)
	#fig = sm.graphics.tsaplots.plot_pacf(df['Seasonal First Difference'].iloc[13:],lags=40,ax=ax2)

	from statsmodels.tsa.arima_model import ARIMA

	model=ARIMA(df['Sales'],order=(1,1,1))
	model_fit=model.fit()

	model_fit.aic

	df['forecast']=model_fit.predict(start=90,end=103,dynamic=True)
	#df[['Sales','forecast']].plot(figsize=(12,8))

	import statsmodels.api as sm

	model=sm.tsa.statespace.SARIMAX(df['Sales'],order=(1, 1, 1),seasonal_order=(1,1,1,12))
	results=model.fit()

	df['forecast']=results.predict(start=90,end=103,dynamic=True)
	#df[['Sales','forecast']].plot(figsize=(12,8))

	from pandas.tseries.offsets import DateOffset
	future_dates=[df.index[-1]+ DateOffset(months=x)for x in range(0,60)]

	future_datest_df=pd.DataFrame(index=future_dates[1:],columns=df.columns)

	future_datest_df.tail()

	future_df=pd.concat([df,future_datest_df])

	future_df['forecast'] = results.predict(start = 104, end = 1000, dynamic= True)  
	future_df[['Sales', 'forecast']].plot(figsize=(12, 8))
	plt.savefig('static/yo.png')
	plt.show()

  


	



