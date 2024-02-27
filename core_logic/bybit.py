# import requests

# def fetch_bybit_ticker(symbol):
#     url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}USDT"
#     response = requests.get(url)
#     data = response.json()
#     return data['result'][0]['last_price'] if data['result'] else None

# def get_coin_prices(coins):
#     coin_price = {}  # Initialize an empty dictionary to store the coin prices

#     for coin_symbol in coins:
#         price = fetch_bybit_ticker(coin_symbol)
#         if price is not None:
#             coin_price[coin_symbol] = price  # Store the price in the dictionary
#         else:
#             print(f"Error fetching data for {coin_symbol}")

#     return coin_price  # Return the dictionary of coin prices

