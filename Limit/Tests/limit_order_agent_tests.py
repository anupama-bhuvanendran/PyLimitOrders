import unittest
from unittest.mock import MagicMock
from ..limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient, ExecutionException

class LimitOrderAgentTest(unittest.TestCase):

    def setUp(self):
        self.mock_execution_client = MagicMock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_add_and_execute_buy_order(self):
        # Add a buy order for 1000 shares of IBM at a limit price of $100
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 99)
        self.mock_execution_client.buy.assert_called_once_with('IBM', 1000)

    def test_add_and_execute_sell_order(self):
        # Add a sell order for 1000 shares of IBM at a limit price of $150
        self.agent.add_order('sell', 'IBM', 1000, 150)
        self.agent.on_price_tick('IBM', 151)
        self.mock_execution_client.sell.assert_called_once_with('IBM', 1000)

    def test_order_not_executed_if_price_not_met(self):
        # Add a buy order for 1000 shares of IBM at a limit price of $100
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.agent.on_price_tick('IBM', 101)
        self.mock_execution_client.buy.assert_not_called()

    def test_handle_execution_exception(self):
        # Add a buy order for 1000 shares of IBM at a limit price of $100
        self.agent.add_order('buy', 'IBM', 1000, 100)
        self.mock_execution_client.buy.side_effect = ExecutionException("Test exception")
        self.agent.on_price_tick('IBM', 99)
        self.mock_execution_client.buy.assert_called_once_with('IBM', 1000)

        self.assertEqual(len(self.agent.orders), 1)


if __name__ == '__main__':
    unittest.main()
