# HistoricalEquityPerformance
Developed a script that uses RapidAPI to gather historical stock data and generate graphs of average monthly returns.

The script makes API calls to RapidAPI to retrieve historical stock data. Saving the data to a local SQLite database to increase performance. It then calculates the average monthly return for each stock and generates a graph of the results. The graphs can be used to visualize the performance of different stocks over time and to identify potential investment opportunities.

Here are some of the benefits of using this service:

* It is easy to use. 
* You can simply provide the ticker symbols of the stocks you want to track and the service will do the rest.
* It is as accurate as you want. The data is retrieved directly from RapidAPI, which is a reliable source of historical stock data. You can choose the number of years to take into account to calculate monthly return.
* It is visual. The graphs make it easy to see the performance of different stocks over time.
* If you are interested in finding the historial performance of stocks to help you decide what to invest in, the graphs are accurate and visual.

* Requirements:
* RapidApi offers up to 500 API free calls a month, all you need is to create an account and input your key where it says YOUR_OWN_KEY.

Design:
1. User inputs number of years and list of stock tickers.
2. Script creates a panda dataframe, saves data historical data in excel file.
3. Creates graph showing monthly return for each ticker
4. Outputs the pdf containing all graphs

Output Snapshot:

<img width="757" alt="image" src="https://github.com/xjefrod99/HistoricalEqPer/assets/52290399/eade8793-8edc-49fc-97fa-b952782bd4d2">

Red ---- shows the yearly average return to be used as baseline.
<img width="763" alt="image" src="https://github.com/xjefrod99/HistoricalEqPer/assets/52290399/fae2991d-373b-4e79-9cbc-fd9645dd6214">

<img width="761" alt="image" src="https://github.com/xjefrod99/HistoricalEqPer/assets/52290399/3de7ace3-6f77-4723-a059-f5dcd5e7126b">

Future work:
! I want to implement https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/ and https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/ so it can provide you a sorted pdf with the stocks that are best fitted to buy right now at the top.



