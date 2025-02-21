import unittest
from unittest.mock import patch
from engine.market_simulator import MarketSimulator


class TestMarketSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = MarketSimulator(epochs=10, initial_price=100.0, volatility=0.01, decay=0.7)

    @patch("numpy.random.normal")
    def test(self, mock_normal):
        mock_normal.side_effect = lambda mean, std: mean

        # Verify parameters:
        self.assertEqual(self.sim.epoch, 0)
        self.assertEqual(self.sim.epochs, 10)
        self.assertEqual(self.sim.price[0], 100.0)
        self.assertEqual(self.sim.volatility, 0.01)
        self.assertEqual(self.sim.decay, 0.7)
        # Verify all arrays are initialized to zero.
        self.assertEqual(self.sim.trading_volume[0], 0)
        self.assertEqual(self.sim.order_flow[0], 0)
        self.assertEqual(self.sim.jitter[0], 0)
        self.assertEqual(self.sim.surge[0], 0)
        self.assertEqual(self.sim.dispersion[0], 0)
        self.assertEqual(self.sim.sentiment[0], 0)
        self.assertEqual(self.sim.log_return[0], 0)

        # Zero volume:
        self.sim.get_next_price(buy_volume=0, sell_volume=0)
        self.assertEqual(self.sim.epoch, 1)
        self.assertEqual(self.sim.trading_volume[1], 1)
        self.assertEqual(self.sim.order_flow[1], 0)
        self.assertEqual(self.sim.jitter[1], self.sim.volatility)
        self.assertEqual(self.sim.surge[1], 0)
        self.assertEqual(self.sim.dispersion[1], self.sim.volatility * (1 - self.sim.decay))
        self.assertEqual(self.sim.sentiment[1], 0)
        self.assertEqual(self.sim.price[1], self.sim.price[0])

        # Jitter == volatility until 3 epochs with trading volume > 0:
        for i in range(2, 6):
            self.sim.get_next_price(buy_volume=10, sell_volume=10)
            self.assertEqual(self.sim.epoch, i)
            (self.assertEqual if i <= 4 else self.assertLess)(self.sim.jitter[i], self.sim.volatility)

        # Positive order flow:
        self.sim.get_next_price(buy_volume=1, sell_volume=0)
        self.assertEqual(self.sim.epoch, 6)
        self.assertEqual(self.sim.order_flow[6], 1)
        self.assertEqual(self.sim.trading_volume[6], 1)
        self.assertGreater(self.sim.price[6], self.sim.price[5])

        # Negative order flow:
        self.sim.get_next_price(buy_volume=0, sell_volume=1)
        self.assertEqual(self.sim.epoch, 7)
        self.assertEqual(self.sim.order_flow[7], -1)
        self.assertEqual(self.sim.trading_volume[7], 1)
        self.assertLess(self.sim.price[7], self.sim.price[6])

        # Very high even volume
        self.sim.get_next_price(buy_volume=1000, sell_volume=1000)
        self.assertEqual(self.sim.epoch, 8)
        self.assertEqual(self.sim.order_flow[8], 0)
        self.assertEqual(self.sim.trading_volume[8], 2000)
        self.assertAlmostEqual(self.sim.jitter[8], 0)
        self.assertAlmostEqual(self.sim.surge[8], 0)

        # Very high uneven volume
        self.sim.get_next_price(buy_volume=1000, sell_volume=0)
        self.assertEqual(self.sim.epoch, 9)
        self.assertEqual(self.sim.order_flow[9], 1000)
        self.assertEqual(self.sim.trading_volume[9], 1000)
        self.assertAlmostEqual(self.sim.jitter[9], 0)
        self.assertAlmostEqual(self.sim.surge[9], self.sim.volatility)

        # Check long term memory:
        self.assertGreater(self.sim.dispersion[9], 0)
        self.assertGreater(self.sim.sentiment[9], 0)

        # Check end of simulation:
        with self.assertRaises(IndexError):
            self.sim.get_next_price(buy_volume=1000, sell_volume=0)


if __name__ == "__main__":
    unittest.main()
