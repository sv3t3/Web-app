import os
from datetime import datetime
import json
from not_bybit import coin_prices
from bybit import get_coin_prices

# Database file interaction
database_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'database.json') # Path to the database.json file
portfolio_value_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'portfolio_value.txt') # Absolute path to the portfolio_value.txt file
os.makedirs(os.path.dirname(database_file_path), exist_ok=True) # Ensure the directory for database_file_path exists
os.makedirs(os.path.dirname(portfolio_value_file_path), exist_ok=True) # Ensure the directory for portfolio_value_file_path exists

# Check if the database file exists
if os.path.exists(database_file_path):
    # Load the data from the file
    with open(database_file_path, 'r') as f:
        data = json.load(f)
    selected_exchange = data['exchange']
    coins = data['coins']
    holdings = data['holdings']

    # Fetch the prices for each coin
    if selected_exchange == "bybit":
        prices = get_coin_prices(coins)
    else:
        prices = {coin: coin_prices(selected_exchange, coin) for coin in coins}

    print(prices)
else:
    selected_exchange = input("Please chose the exchange: ").lower()

    if selected_exchange == "bybit":
        coins_input = input("Enter the coins in your portfolio (separated by a comma): ")
        coins = [coin.strip().upper() for coin in coins_input.split(',')]  # Create a list with the user's coins
        prices = get_coin_prices(coins)
    else:
        another_exchange = selected_exchange  # Ask user to input an exchange
        coins_input = input("Enter the coins in your portfolio (separated by a comma): ")
        coins = [coin.strip().upper() for coin in coins_input.split(',')]  # Create a list with the user's coins
        prices = {coin: coin_prices(another_exchange, coin) for coin in coins}  # Fetch the prices for each coin

    #print(prices)

    holdings = {coin: float(input(f"Enter the amount of {coin} you hold: ")) for coin in coins} # Ask the user for the amount of each coin they hold

# Calculate the total value of the user's holdings, value of each coin and the total portfolio value
total_values = {coin: amount * float(prices[coin]) for coin, amount in holdings.items()}
total_portfolio_value = sum(total_values.values())

# txt file management
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(portfolio_value_file_path, 'a') as f:
    f.write(f'{timestamp}: {round(total_portfolio_value, 2)}\n') # Write the timestamp and portfolio value to a text file

# Json data storage
data = {
    'exchange': selected_exchange,
    'coins': coins,
    'holdings': holdings,
    'total_values': total_values,
    'total_portfolio_value': total_portfolio_value,
}

with open(database_file_path, 'w') as f: # Write the data to the database.json file
    json.dump(data, f)

print(f"The total value of your holdings is {(total_values)}")
print(f"The total value of your portfolio is {round(total_portfolio_value, 2)} USDT")