
import datetime
import requests
import pandas as pd

key = 'YOUR_OWN_KEY'

url = "https://apistocks.p.rapidapi.com/weekly"

symbol = ["BNO", "AGG", "ACC"]

querystring = {"symbol":symbol,"dateStart":"2020-01-01","dateEnd":"2022-12-31"}

headers = {
	"X-RapidAPI-Key": "YOUR_OWN_KEY",
	"X-RapidAPI-Host": "apistocks.p.rapidapi.com"
}


response = requests.request("GET", url, headers=headers, params=querystring).json()


data = response['Results']
df = pd.DataFrame(data)
import numpy as np

params = ['symbol', 'year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
monthly_return = []
temp = []

df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['MonthDiff'] = df['Month'].diff()

# remove rows where year is less than 2020
df = df[df['Year'] >= 2020]

# loop through each year
for year in df['Year'].unique():
    year_data = df[df['Year'] == year]

    # loop through each month
    for month in range(1, 13):
        month_data = year_data[year_data['Month'] == month]

        # calculate monthly return
        if len(month_data) > 0:
            adj_close = month_data['AdjClose'].values
            month_return = np.append(0, (adj_close[-1:] - adj_close[1:]) / adj_close[1:])
            month_return[np.isinf(month_return)] = 0
            temp.extend(month_return)

    if len(temp) > 0:
        temp = [symbol, year] + temp
        temp_dict = dict(zip(params, temp))
        monthly_return.append(temp_dict)
        temp = []


monthly_return


month_df = pd.DataFrame(monthly_return)








