from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener
from trading_framework.execution_client import ExecutionException





class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        super().__init__()
        self.execution_client = execution_client
        self.orders = []  

    def add_order(self, buy_sell_flag: str, product_id: str, amount: int, limit: float):
        order = {
            'buy_sell_flag': buy_sell_flag,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        }
        self.orders.append(order)

    def on_price_tick(self, product_id: str, price: float):
        
        # Create a list to hold orders that will be removed after execution
        orders_to_remove = []
        
        # Check each order to see if it can be executed
        for order in self.orders:
            if order['product_id'] == product_id:
                try:
                    if order['buy_sell_flag'] == 'buy' and price <= order['limit']:
                        self.execution_client.buy(product_id, order['amount'])
                        orders_to_remove.append(order)
                    elif order['buy_sell_flag'] == 'sell' and price >= order['limit']:
                        self.execution_client.sell(product_id, order['amount'])
                        orders_to_remove.append(order)
                except ExecutionException as e:
                    print(f"Failed to execute {'buy' if order['buy_sell_flag'] == 'buy' else 'sell'} order: {e}")
        
        # Remove executed orders from the list
        for order in orders_to_remove:
            self.orders.remove(order)
