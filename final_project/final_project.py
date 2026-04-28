
"""
Final project, Data 5500, Quinton Latimer
"""

import json
import requests
import time
import os

"""
------ Alpaca paper trading keys -------
"""
ALPACA_API_KEY = "PKZO7ALI6ZOHGLFORDYXC2FSYI"
ALPACA_SECRET_KEY = "6KMVbXqEC5ESkXfNJp3FzFEdzHTt85K6Xs58tKGTR51a"

"""
------ folder path -----
"""
folder_path = "/home/ubuntu/data5500_spring2026/data5500_mycode/final_project/data/"

"""
-------------------- Function 1 to decide if a csv file should be updated or created --------------------
"""
def create_or_update_csv(ticker):
    file_path = folder_path + ticker + ".csv"
    try:
        # Check if the file exists AND has data inside
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            print("Updating " + ticker + " file")
            append_data(ticker)
        else:
            print("File for " + ticker + " is missing or empty. Creating...")
            initialHistory(ticker)
    except Exception as e:
        print(f"Error handling file for {ticker}: {e}")

"""
-------------------- Function 2 to write initial history (100 days of trading history)--------------------
"""
def initialHistory(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=NG9C9EPVYBMQT0C8'
    req = requests.get(url)
    request_dictionary = json.loads(req.text)
    
    if 'Time Series (Daily)' not in request_dictionary:
        print(f"API Error for {ticker}. Alpha Vantage says: {request_dictionary}")
        return

    key1 = 'Time Series (Daily)'
    key2 = '4. close'
    csv_file = open(folder_path + ticker + '.csv', 'w')
    write_lines = []
    for date in request_dictionary[key1]:
        write_lines.append(date + ',' + request_dictionary[key1][date][key2] + '\n')
    write_lines.reverse()
    csv_file.writelines(write_lines)
    csv_file.close()

"""
-------------------- Function 3 to append data --------------------
"""
def append_data(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + ticker + '&apikey=NG9C9EPVYBMQT0C8'
    req = requests.get(url)
    request_dictionary = json.loads(req.text)
    
    if 'Time Series (Daily)' not in request_dictionary:
        print(f"API Error for {ticker}. Alpha Vantage says: {request_dictionary}")
        return

    key1 = 'Time Series (Daily)'
    key2 = '4. close'
    csv_file = open(folder_path + ticker + '.csv', 'r')
    lines = csv_file.readlines()
    last_date = lines[-1].split(',')[0]
    new_lines = []
    for date in request_dictionary[key1]:
        if date == last_date:
            break
        new_lines.append(date + ',' + request_dictionary[key1][date][key2] + '\n')
    new_lines.reverse()
    csv_file = open(folder_path + ticker + '.csv', 'a')
    csv_file.writelines(new_lines)
    csv_file.close()

"""
-------------------- Function 4 to load prices --------------------
"""
def loadPricesFromCSV(ticker, folder_path):
    prices = []
    try:
        with open(folder_path + ticker + ".csv", "r") as file: 
            for line in file:
                price = float(line.strip().split(",")[1])
                prices.append(round(price, 2))
    except FileNotFoundError:
        print(ticker + ".csv file not found.")
    return prices

"""
-------------------- Function 5 Alpaca paper trading order --------------------
"""
def submit_paper_order(ticker, side):
    url = "https://paper-api.alpaca.markets/v2/orders"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }
    payload = {
        "symbol": ticker,
        "qty": "1",
        "side": side,
        "type": "market",
        "time_in_force": "day"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"***** Successfully submitted Alpaca PAPER order to {side} 1 share of {ticker} *****")
        else:
            print(f"***** Failed to submit Alpaca order. Status: {response.status_code} *****")
    except Exception as e:
        print("***** Error submitting order to Alpaca:", e)

"""
-------------------- Function 6: Mean Reversion --------------------
"""
def meanReversionStrategy(prices, ticker):
    buy_price = None
    sell_price = None
    profit = 0
    trades = []

    for i in range(5, len(prices)):
        moving_avg = round(sum(prices[i-5:i]) / 5, 2)
        price = prices[i]
        
        #buy 
        if price < moving_avg * 0.98:
            if sell_price is not None:
                trade_profit = round(sell_price - price, 2)
                profit += trade_profit
                trades.append((sell_price, price))
                sell_price = None
            elif buy_price is None:
                buy_price = price
        #sell
        elif price > moving_avg * 1.02:
            if buy_price is not None:
                trade_profit = round(price - buy_price, 2)
                profit += trade_profit
                trades.append((buy_price, price))
                buy_price = None
            #short
            elif sell_price is None:
                sell_price = price

    if trades:
        percent_return = round((profit / trades[0][0]) * 100, 2)
    else:
        percent_return = 0

    mostRecentAvg = round(sum(prices[-5:]) / 5, 2)
    mostRecentPrice = prices[-1]
    
    if mostRecentPrice < mostRecentAvg * 0.98:
        print(f"You should buy {ticker} today")
        submit_paper_order(ticker, "buy")
    elif mostRecentPrice > mostRecentAvg * 1.02:
        print(f"You should sell {ticker} today")
        submit_paper_order(ticker, "sell")
    else:
        print("Signal:\t none today")

    return round(profit, 2), percent_return

"""
-------------------- Function 7: Simple Moving Average --------------------
"""
def simpleMovingAverageStrategy(prices, ticker):
    buy_price = None
    sell_price = None
    profit = 0
    trades = []

    for i in range(5, len(prices)):
        moving_avg = round(sum(prices[i-5:i]) / 5, 2)
        price = prices[i]
        
        #buy
        if price > moving_avg:
            if sell_price is not None:
                trade_profit = round(sell_price - price, 2)
                profit += trade_profit
                trades.append((sell_price, price))
                sell_price = None
            elif buy_price is None:
                buy_price = price
        #sell
        elif price < moving_avg:
            if buy_price is not None:
                trade_profit = round(price - buy_price, 2)
                profit += trade_profit
                trades.append((buy_price, price))
                buy_price = None
            #short
            elif sell_price is None:
                sell_price = price

    if trades:
        percent_return = round((profit / trades[0][0]) * 100, 2) 
    else:
        percent_return = 0
        
    mostRecentAvg = round(sum(prices[-5:]) / 5, 2)
    mostRecentPrice = prices[-1]
    
    if mostRecentPrice > mostRecentAvg:
        print(f"You should buy {ticker} today")
        submit_paper_order(ticker, "buy")
    elif mostRecentPrice < mostRecentAvg:
        print(f"You should sell {ticker} today")
        submit_paper_order(ticker, "sell")

    return round(profit, 2), percent_return

"""
-------------------- Function 8: Bollinger Bands --------------------
"""
def bollingerBandsStrategy(prices, ticker):
    buy_price = None
    sell_price = None
    profit = 0
    trades = []

    for i in range(20, len(prices)):
        moving_avg = round(sum(prices[i-20:i]) / 20, 2)
        price = prices[i]
        
        #buy
        if price < moving_avg * 0.95: 
            if sell_price is not None:
                trade_profit = round(sell_price - price, 2)
                profit += trade_profit
                trades.append((sell_price, price))
                sell_price = None
            elif buy_price is None:
                buy_price = price

        #sell
        elif price > moving_avg * 1.05:
            if buy_price is not None:
                trade_profit = round(price - buy_price, 2)
                profit += trade_profit
                trades.append((buy_price, price))
                buy_price = None
            #short
            elif sell_price is None:
                sell_price = price

    if trades:
        percent_return = round((profit / trades[0][0]) * 100, 2)
    else:
        percent_return = 0

    mostRecentAvg = round(sum(prices[-20:]) / 20, 2)
    mostRecentPrice = prices[-1]
    
    if mostRecentPrice < mostRecentAvg * 0.95:
        print(f"You should buy {ticker} today")
        submit_paper_order(ticker, "buy")
    elif mostRecentPrice > mostRecentAvg * 1.05:
        print(f"You should sell {ticker} today")
        submit_paper_order(ticker, "sell")

    return round(profit, 2), percent_return

"""
-------------------- Function 9 to save results to JSON file --------------------
"""
def saveResults(results):
    with open("/home/ubuntu/data5500_spring2026/data5500_mycode/final_project/results.json", "w") as file:
        json.dump(results, file, indent=4)

"""
-------------------- Main code body --------------------
"""
tickers = ["AAPL", "GOOG", "ADBE", "MSFT", "VZ", "NVDA", "AMZN", "NFLX", "BA", "JPM"]
results = {}

mostProfitable = -999999
bestStock = ""
bestStrat = ""

for ticker in tickers:
    create_or_update_csv(ticker)
    try:
        prices = loadPricesFromCSV(ticker, folder_path)
        if len(prices) > 20: 
            results[ticker + "_prices"] = prices

            print("\n" + ticker + " Mean Reversion Strategy Output:")
            mr_profit, mr_returns = meanReversionStrategy(prices, ticker)
            results[ticker + "_mr_profit"] = mr_profit
            results[ticker + "_mr_returns"] = mr_returns

            print("\n" + ticker + " Simple Moving Average Strategy Output:")
            sma_profit, sma_returns = simpleMovingAverageStrategy(prices, ticker)
            results[ticker + "_sma_profit"] = sma_profit
            results[ticker + "_sma_returns"] = sma_returns

            print("\n" + ticker + " Bollinger Bands Strategy Output:")
            bb_profit, bb_returns = bollingerBandsStrategy(prices, ticker)
            results[ticker + "_bb_profit"] = bb_profit
            results[ticker + "_bb_returns"] = bb_returns

            if mr_profit > mostProfitable:
                mostProfitable = mr_profit
                bestStock = ticker
                bestStrat = "Mean reversion"

            if sma_profit > mostProfitable:
                mostProfitable = sma_profit
                bestStock = ticker
                bestStrat = "Simple moving average"

            if bb_profit > mostProfitable:
                mostProfitable = bb_profit
                bestStock = ticker
                bestStrat = "Bollinger bands"
        else:
            print(f"Not enough data to run strategies for {ticker}.")

    except FileNotFoundError:
        print("File for " + ticker + " not found. Skipping " + ticker)

    print(f"\nPausing for 15 seconds for API limits...")
    time.sleep(15)

results["Best stock"] = bestStock
results["Best strategy"] = bestStrat
results["Best profit"] = round(mostProfitable, 2)

print("\n")
print("-----------------------")
print("Best overall stock performance and strategy for this analysis:")
print("Stock:","\t",bestStock)
print("Strategy:","\t",bestStrat)
print("Profit: $","\t",round(mostProfitable, 2))
print("-----------------------")
print("\n")

saveResults(results)