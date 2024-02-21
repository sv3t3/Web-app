import ccxt


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
