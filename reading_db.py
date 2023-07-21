#/Users/jeff/Desktop/analysis/monthly_returns.db

import sqlite3
import pandas as pd
import numpy as np
# Connect to the database
conn = sqlite3.connect('/Users/jeff/Desktop/analysis/monthly_returns.db')


import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
df = pd.read_csv('output.csv')

# Convert year and month columns to datetime
# Compute average monthly returns for each symbol
symbol_returns = {}
for symbol in df['symbol'].unique():
    symbol_df = df[df['symbol'] == symbol]
    avg_returns = symbol_df.iloc[:, 2:].mean().reset_index()
    avg_returns.columns = ["month", "avg_return"]
    symbol_returns[symbol] = avg_returns

# Plot average monthly returns for each symbol and save to PDF
with PdfPages('monthly_returns.pdf') as pdf:
    for symbol, data in symbol_returns.items():
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot( data['month'], data['avg_return'], 'o-')

        # plot avg of avg_return
        avg_avg_return = data['avg_return'].mean()
        ax.axhline(avg_avg_return, color='red', linestyle='--', label='Average of Average Return')


        ax.plot(np.mean(data['avg_return']), '--')
        ax.set_title(symbol)
        ax.set_xlabel('Month')
        ax.set_ylabel('Avg. Return')
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.axhline(0, color='black', lw=1)
        plt.xticks(rotation=45, ha='right')
        pdf.savefig(fig)
        plt.close(fig)
