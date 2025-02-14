import unittest
from engine.market_simulator import get_next_price


class test_next_price(unittest.TestCase):
    def test_all_zero_input(self):
        last_price = 0
        volatility = 0
        buy_volume = 0
        sell_volume = 0
        next_price = get_next_price(last_price, volatility, buy_volume, sell_volume)
        self.assertIsInstance(next_price, float)
        self.assertEqual(next_price, last_price)

    def test_high_pos_order_flow(self):
        last_price = 1
        volatility = 0.01
        buy_volume = 100
        sell_volume = 0

        next_price = get_next_price(last_price, volatility, buy_volume, sell_volume)

        self.assertIsInstance(next_price, float)
        self.assertGreater(next_price, last_price)

    def test_high_neg_order_flow(self):
        last_price = 1
        volatility = 0.01
        buy_volume = 0
        sell_volume = 100

        next_price = get_next_price(last_price, volatility, buy_volume, sell_volume)

        self.assertIsInstance(next_price, float)
        self.assertLess(next_price, last_price)

    def test_high_vs_low_volatility(self):
        last_price = 1
        volatility = 1
        low_buy = 0
        low_sell = 0
        high_buy = 1000
        high_sell = 1000

        low_vol_price = get_next_price(last_price, volatility, high_buy, high_sell)
        high_vol_price = get_next_price(last_price, volatility, low_buy, low_sell)

        self.assertIsInstance(low_vol_price, float)
        self.assertIsInstance(high_vol_price, float)
        self.assertGreater(abs(high_vol_price - last_price), abs(low_vol_price - last_price))


if __name__ == "__main__":
    unittest.main()
