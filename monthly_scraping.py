import requests
import pandas as pd
import numpy as np
import sqlite3

#STEP 2
l = "https://apistocks.p.rapidapi.com/weekly"

with open('appendix2.txt', 'r') as f:
    symbol = [line.strip() for line in f]


# # df = pd.DataFrame(data)
# data.to_csv('saving_api_data.csv', index=False)

df = pd.read_csv("saving_api_data.csv")
# Convert Date to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
 

params = ['symbol', 'year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
# Remove rows where year is less than 2001
df = df[df['Year'] >= 2009]
# Initialize empty list to store monthly return dictionaries
monthly_return = []

symbol = df['Symbol'].unique()
# Loop through each symbol
c = 1
for sym in symbol:
    print(c, ":", len(symbol))
    c+=1
    sym_data = df[df['Symbol'] == sym].copy()


    # Loop through each year
    for year in sym_data['Year'].unique():
        year_data = sym_data[sym_data['Year'] == year]

        # Initialize empty list to store monthly returns
        monthly_returns_list = []

        # Loop through each month
        for month in range(1, 13):
            month_data = year_data[year_data['Month'] == month]

            # Calculate monthly return
            if len(month_data) > 0:
                adj_close = month_data['AdjClose'].values
                month_return = np.array((adj_close[-1] / adj_close[0]) -1)
                month_return[np.isinf(month_return)] = 0
                month_return[np.isnan(month_return)] = 0
                monthly_returns_list.append(month_return)

        # Create dictionary for monthly returns
        monthly_returns_dict = {'symbol': sym, 'year': year}
        for i, val in enumerate(monthly_returns_list):
            if i < len(params) - 2:
                monthly_returns_dict[params[i + 2]] = val

        # Append monthly returns dictionary to list
        monthly_return.append(monthly_returns_dict)
        monthly_returns_dict = {}

# Create dataframe from monthly return list
monthly_return_df = pd.DataFrame(monthly_return)
print("finished gathering data...")
# Create a connection to the database (this will create a new database if it doesn't exist)
conn = sqlite3.connect('monthly_returns.db')

# Convert the dataframe to a SQLite table
monthly_return_df.to_sql('monthly_returns', conn, if_exists='replace', index=False)
monthly_return_df.to_csv('output.csv', index=False)
# Close the connection
conn.close()
