import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import style

#grab daily data
#set aside 20% of data

import requests

sym = "GLCN"
data = pd.DataFrame({})
url = "https://quotient.p.rapidapi.com/equity/daily"

querystring = {"symbol":sym,"from":"2002-03-01","to":"2023-04-15","adjust":"false"}

headers = {
	"X-RapidAPI-Key": "3730dcc5f4msh5211faf2fd9d189p1245dfjsn9ef5f086f353",
	"X-RapidAPI-Host": "quotient.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
res = response.json()
print(response.text)

temp_df = pd.DataFrame(res)
temp_df['Symbol'] = sym
data = pd.concat([data, temp_df])

name = "{}_20_year_daily.csv".format(sym)
data.to_csv(name, index=False)


#do analysis for the last 20 years, but dev only w 20% of the data

#set aside 20% of data as test data
df = pd.read_csv('saving_api_data.csv')

data = df[df['Symbol']==symbol]

close_px = data['AdjClose']
mavg_50 = close_px.rolling(window=8).mean().dropna()

mavg_200 = close_px.rolling(window=28).mean().dropna()


# Adjusting the style of matplotlib
style.use('ggplot')

close_px.plot(label=symbol)
mavg_50.plot(label='mavg_50')
mavg_200.plot(label='mavg_200')

plt.legend()


rets = close_px / close_px.shift(1) - 1
rets.plot(label='return')


# Define the short-term (14-day) and long-term (28-day) exponential moving averages
ema14 = data['Close'].ewm(span=2, adjust=False).mean().dropna()
ema28 = data['Close'].ewm(span=7, adjust=False).mean().dropna()

macd = ema14 - ema28

#use 9 days in future
signal = macd.ewm(span=2, adjust=False).mean()
histogram = macd - signal


# Calculate the relative strength index (RSI) over a 14-day period
delta = data['AdjClose'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=3).mean().dropna()
avg_loss = loss.rolling(window=3).mean().dropna()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# Calculate the historical returns over a specific time period
time_period = 12  # 90 days
data['Returns'] = data['AdjClose'].pct_change(periods=time_period).dropna()

data = data.replace([np.inf, -np.inf], 999)

data.fillna(value=0, inplace=True)


data['Target'] = 0
data.loc[(rsi < 30) & (histogram > 0) & (data['Returns'] > 0), 'Target'] = 1
data.loc[(rsi > 70) & (histogram < 0) & (data['Returns'] < 0), 'Target'] = -1
