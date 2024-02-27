# Import necessary libraries
import os
import ccxt
import requests
from datetime import datetime
import json

# Function to fetch the latest price of a given symbol from Bybit
def fetch_bybit_ticker(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    return data['result'][0]['last_price'] if data['result'] else None

# Function to get the prices of multiple coins from Bybit
def get_coin_prices(coins):
    coin_price = {}  # Initialize an empty dictionary to store the coin prices

    for coin_symbol in coins:
        price = fetch_bybit_ticker(coin_symbol)
        if price is not None:
            coin_price[coin_symbol] = price  # Store the price in the dictionary
        else:
            print(f"Error fetching data for {coin_symbol}")

    return coin_price  # Return the dictionary of coin prices

# Function to get the price of a coin from a given exchange using ccxt library
def coin_prices(exchange, coin):
    coin_prices = {}  # Initialize an empty dictionary to store the coin prices

    # Check if the entered exchange is valid
    if exchange not in ccxt.exchanges:
        print("Invalid exchange.")
    else:
        # Initialize the selected exchange
        exchange = getattr(ccxt, exchange)()

        # Fetch and store the current price of 'coin'
        try:
            ticker = exchange.fetch_ticker(coin + '/USDT')
            coin_prices[coin] = ticker['last']  # Store the price in the dictionary
        except Exception as e:
            print(f"An error occurred: {e}")

    return coin_prices  # Return the dictionary of coin prices

# Function to calculate the total value of a portfolio
def calculate_portfolio_value(exchange, holdings):
    # Database file interaction
    database_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'database.json') # Path to the database.json file
    portfolio_value_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'portfolio_value.txt') # Absolute path to the portfolio_value.txt file
    os.makedirs(os.path.dirname(database_file_path), exist_ok=True) # Ensure the directory for database_file_path exists
    os.makedirs(os.path.dirname(portfolio_value_file_path), exist_ok=True) # Ensure the directory for portfolio_value_file_path exists

    coins = list(holdings.keys())

    # Fetch the prices for each coin
    if exchange == "bybit":
        prices = get_coin_prices(coins)
    else:
        prices = {coin: coin_prices(exchange, coin) for coin in coins}

    # Calculate the total value of the user's holdings, value of each coin and the total portfolio value
    total_values = {coin: amount * float(prices[coin]) for coin, amount in holdings.items()}
    total_portfolio_value = sum(total_values.values())

    # txt file management
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(portfolio_value_file_path, 'a') as f:
        f.write(f'{timestamp}: {round(total_portfolio_value, 2)}\n') # Write the timestamp and portfolio value to a text file

    # Json data storage
    data = {
        'exchange': exchange,
        'coins': coins,
        'holdings': holdings,
        'total_values': total_values,
        'total_portfolio_value': total_portfolio_value,
    }

    with open(database_file_path, 'w') as f: # Write the data to the database.json file
        json.dump(data, f)

    return round(total_portfolio_value, 2)


# 1.) fetch_bybit_ticker(symbol): This function fetches the latest 
#     price of a given symbol from Bybit.

# 2.) get_coin_prices(coins): This function uses the fetch_bybit_ticker(symbol) function 
#     to get the prices of multiple coins from Bybit.

# 3.) coin_prices(exchange, coin): This function uses the ccxt library to get the price of a coin from a given exchange.

# 4.) calculate_portfolio_value(exchange, holdings): This function calculates the total 
#     value of a portfolio based on the holdings and the current prices of the coins. 
#     It fetches the prices using either the get_coin_prices(coins) function or the coin_prices(exchange, coin) function 
#     depending on the exchange. It also writes the portfolio value to a text file and the portfolio data to a JSON file.






































# # exchange.py
# import os
# from datetime import datetime
# import json
# from not_bybit import coin_prices
# from bybit import get_coin_prices

# def calculate_portfolio_value(exchange, holdings):
#     # Database file interaction
#     database_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'database.json') # Path to the database.json file
#     portfolio_value_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'portfolio_value.txt') # Absolute path to the portfolio_value.txt file
#     os.makedirs(os.path.dirname(database_file_path), exist_ok=True) # Ensure the directory for database_file_path exists
#     os.makedirs(os.path.dirname(portfolio_value_file_path), exist_ok=True) # Ensure the directory for portfolio_value_file_path exists

#     coins = list(holdings.keys())

#     # Fetch the prices for each coin
#     if exchange == "bybit":
#         prices = get_coin_prices(coins)
#     else:
#         prices = {coin: coin_prices(exchange, coin) for coin in coins}

#     # Calculate the total value of the user's holdings, value of each coin and the total portfolio value
#     total_values = {coin: amount * float(prices[coin]) for coin, amount in holdings.items()}
#     total_portfolio_value = sum(total_values.values())

#     # txt file management
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     with open(portfolio_value_file_path, 'a') as f:
#         f.write(f'{timestamp}: {round(total_portfolio_value, 2)}\n') # Write the timestamp and portfolio value to a text file

#     # Json data storage
#     data = {
#         'exchange': exchange,
#         'coins': coins,
#         'holdings': holdings,
#         'total_values': total_values,
#         'total_portfolio_value': total_portfolio_value,
#     }

#     with open(database_file_path, 'w') as f: # Write the data to the database.json file
#         json.dump(data, f)

#     return round(total_portfolio_value, 2)

# # 24h, 7d, 30d growth
# # Best performing coin