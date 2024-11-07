import time
from web3 import Web3
import numpy as np

def fetch_prices(dexes, token_pair):
    prices = {}
    for dex in dexes:
        prices[dex] = dex.get_price(token_pair)
    return prices

def calculate_arbitrage_opportunity(prices):
    max_price_dex, max_price = max(prices.items(), key=lambda x: x[1])
    min_price_dex, min_price = min(prices.items(), key=lambda x: x[1])
    
    potential_profit = (max_price - min_price) - estimate_fees(max_price, min_price)
    
    if potential_profit > 0:
        return min_price_dex, max_price_dex, potential_profit
    return None

def execute_arbitrage(buy_dex, sell_dex, token_pair, amount):
    # Execute buy and sell on respective DEXs
    buy_tx = buy_dex.buy(token_pair, amount)
    sell_tx = sell_dex.sell(token_pair, amount)
    return buy_tx, sell_tx

def run_bot():
    dexes = [Uniswap(), Sushiswap(), Balancer()]
    token_pair = "ETH/USDT"
    
    while True:
        prices = fetch_prices(dexes, token_pair)
        opportunity = calculate_arbitrage_opportunity(prices)
        
        if opportunity:
            buy_dex, sell_dex, profit = opportunity
            execute_arbitrage(buy_dex, sell_dex, token_pair, amount)
        time.sleep(5)

run_bot()
