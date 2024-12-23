import unittest
from datetime import datetime, timedelta
from stock import Stock, GBCE, Trade

class TestStock(unittest.TestCase):
    def setUp(self):
        self.tea = Stock('TEA', 'Common', 0, 0, 100)
        self.pop = Stock('POP', 'Common', 8, 0, 100)
        self.ale = Stock('ALE', 'Common', 23, 0, 60)
        self.gin = Stock('GIN', 'Preferred', 8, 2, 100)
        self.joe = Stock('JOE', 'Common', 13, 0, 250)
        self.stocks = [self.tea, self.pop, self.ale, self.gin, self.joe]
        self.gbce = GBCE()
        for stock in self.stocks:
            self.gbce.add_stocks(stock)

    def test_dividend_yield(self):
        self.assertEqual(self.pop.calculate_dividend_yield(100), 0.08)
        self.assertEqual(self.gin.calculate_dividend_yield(100), 2.0)

    def test_pe_ratio(self):
        self.assertEqual(self.pop.calculate_pe_ratio(100), 12.5)
        self.assertEqual(self.gin.calculate_pe_ratio(100), 12.5)

    def test_record_trade(self):
        self.pop.record_trade(datetime.now(), 100, "buy", 105)
        self.assertEqual(len(self.pop.trades), 1)
        self.assertEqual(self.pop.trades[0].quantity, 100)
        self.assertEqual(self.pop.trades[0].price, 105)

    def test_volume_weighted_stock_price(self):
        now = datetime.now()
        self.pop.record_trade(now, 100, "buy", 105)
        self.pop.record_trade(now - timedelta(minutes=4), 200, "buy", 110)
        self.pop.record_trade(now - timedelta(minutes=5), 200, "buy", 210)
        self.pop.record_trade(now - timedelta(minutes=6), 300, "buy", 115)  # This trade should be ignored
        self.assertAlmostEqual(self.pop.calculate_volume_weighted_stock_price(), 149.00, places=2)

    def test_gbce_all_share_index_no_trades(self):
        now = datetime.now()
        self.pop.record_trade(now - timedelta(minutes=6), 300, "buy", 115)
        self.assertEqual(self.gbce.calculate_all_share_index(), 0)

    def test_gbce_all_share_index_no_trade(self):
        self.assertEqual(self.gbce.calculate_all_share_index(), 0)

    """
    Calculates the all share index with trades from the last 5 minutes
    """
    def test_gbce_all_share_index(self):
        # Record individual trades for each stock
        now = datetime.now()
        trades = [
            (self.tea, now, 100, "buy", 234),
            (self.tea, now - timedelta(minutes=4), 400, "buy", 200),
            (self.tea, now - timedelta(minutes=5), 250, "buy", 232),
            (self.tea, now - timedelta(minutes=6), 30, "sell", 442),
            (self.pop, now, 100, "buy", 105),
            (self.pop, now - timedelta(minutes=4), 200, "buy", 110),
            (self.pop, now - timedelta(minutes=5), 200, "sell", 210),
            (self.pop, now - timedelta(minutes=6), 300, "buy", 115),
            (self.ale, now, 100, "buy", 105),
            (self.ale, now - timedelta(minutes=4), 200, "buy", 110),
            (self.ale, now - timedelta(minutes=5), 200, "buy", 210),
            (self.ale, now - timedelta(minutes=6), 300, "buy", 115),
            (self.gin, now, 100, "buy", 105),
            (self.gin, now - timedelta(minutes=4), 200, "buy", 300),
            (self.gin, now - timedelta(minutes=5), 200, "buy", 122),
            (self.gin, now - timedelta(minutes=6), 300, "sell", 600),
            (self.joe, now, 100, "buy", 105),
            (self.joe, now - timedelta(minutes=4), 200, "buy", 10),
            (self.joe, now - timedelta(minutes=5), 200, "sell", 27),
            (self.joe, now - timedelta(minutes=6), 300, "buy", 17),
        ]

        for stock, timestamp, quantity, buy_or_sell, price in trades:
                stock.record_trade(timestamp, quantity, buy_or_sell, price)

        self.assertAlmostEqual(self.gbce.calculate_all_share_index(), 126.55, places=2)

if __name__ == '__main__':
    unittest.main()