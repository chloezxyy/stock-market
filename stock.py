from datetime import datetime, timedelta
from prettytable import PrettyTable

import math

class Trade:
    """
    timestamp: datetime object is an optional parameter. If not provided, it will default to the current time
    """
    def __init__(self, quantity, buy_or_sell, price, timestamp=None):
        self.quantity = quantity
        self.buy_or_sell = buy_or_sell
        self.price = price
        self.timestamp = timestamp if timestamp is not None else datetime.now()

class Stock:
    def __init__(self, symbol: str, stock_type: str, last_dividend: float, fixed_dividend: float, par_value: float):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = [] # list of trades for a particular stock

    def calculate_dividend_yield(self, price: float) -> float:
        if price <= 0:
            raise ValueError('Price must be greater than 0') 

        if self.stock_type == 'Common':
            return self.last_dividend / price
        else:
            return (self.fixed_dividend * self.par_value) / price
    
    def calculate_pe_ratio(self, price):
        if self.last_dividend <= 0:
            return float('inf')

        return price / self.last_dividend
    
    def record_trade(self, timestamp: datetime, quantity: int, buy_or_sell: str, price: float) -> None:
        if quantity <= 0 or price <= 0:
            raise ValueError('Quantity must be greater than 0')
        
        new_trade = Trade(quantity, buy_or_sell, price, timestamp)
        self.trades.append(new_trade)

    def calculate_volume_weighted_stock_price(self) -> float:
        cutoff_time = datetime.now() - timedelta(minutes=5)
        # Includes trades that are within the last 5 minutes
        recent_trades = [trade for trade in self.trades if trade.timestamp > cutoff_time - timedelta(seconds=1)]
        total_quantity = sum(trade.quantity for trade in recent_trades)

        if total_quantity == 0:
            return 0
        
        # vwsp = sum(trade1's price * trade1's quantity, trade2's price*trade2's quantity, ...) / sum(trade1's quantity, trade2's quantity, ...) 
        total_trade_value = sum(trade.price * trade.quantity for trade in recent_trades)
        return total_trade_value / total_quantity
    
class GBCE:
    def __init__(self):
        self.stocks = []

    def add_stocks(self, stock: Stock) -> None:
        self.stocks.append(stock)

    """
    Calculate VWSP for each stock: Use only trades from the last 5 minutes
    Calculate the geometric mean of the VWSP of all stocks
        - Formula: n sqrt of the product of vwsp of each stocks in gbce
    """ 
    def calculate_all_share_index(self) -> float:
        vwsp = [stock.calculate_volume_weighted_stock_price() for stock in self.stocks]
        non_zero_prices = [price for price in vwsp if price > 0]

        if not non_zero_prices:
            return 0
        
        # Get the product of all non zero stocks
        prod = math.prod(non_zero_prices)
        return prod ** (1 / len(non_zero_prices))

def main():
    input_price = 100  # Example input price, you can change it as needed

    # Define sample data
    tea = Stock('TEA', 'Common', 0, 0, 100)
    pop = Stock('POP', 'Common', 8, 0, 100)
    ale = Stock('ALE', 'Common', 23, 0, 60)
    gin = Stock('GIN', 'Preferred', 8, 2, 100)
    joe = Stock('JOE', 'Common', 13, 0, 250)

    stocks = [tea, pop, ale, gin, joe]
    gbce = GBCE()
    for stock in stocks:
        gbce.add_stocks(stock)

    """
    Optional: Add your own trades to the stocks
    Refer to test_gbce_all_share_index method in test_stock.py on how to record trades
    """

    # Calculate metrics and print in a table
    table = PrettyTable()
    table.field_names = ["Stock", "Dividend Yield", "P/E Ratio", "Volume Weighted Stock Price"]
    
    for stock in stocks:
        dividend_yield = stock.calculate_dividend_yield(input_price)
        pe_ratio = stock.calculate_pe_ratio(input_price)
        vwsp = stock.calculate_volume_weighted_stock_price()
        table.add_row([stock.symbol, f"{dividend_yield:.2f}", f"{pe_ratio:.2f}", f"{vwsp:.2f}"])

    print(table)
    print(f"GBCE All Share Index: {gbce.calculate_all_share_index():.2f}")

if __name__ == "__main__":
    main()





