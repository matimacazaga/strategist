from options_base import Strategy, Put, Call
import numpy as np 
from stocks_base import Stock

class CoveredPut(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Covered Put')

        self.add_position([(-1, Stock(initial_stock_price)), (-1, Put(strike))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):
        
        if C is None:

            C = self.derivative_price
        
        max_profit = self.initial_stock_price - self.positions[1][1].strike + C

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self):

        print(f'Max Loss: {np.inf}')


class ProtectiveCall(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Protective Call')

        self.add_position([(-1, Stock(initial_stock_price)), (1, Call(strike))])

        self.initial_stock_price = initial_stock_price


if __name__ == '__main__':

    initial_stock_price = 50.

    strategy = CoveredPut(initial_stock_price, 45.)

    params = {'risk_free': 0.05, 'sigma':0.15, 
              'plazo': 180, 'n':1_000_000,
              'seed': 123}

    print(f'Pricing: {strategy.get_price(**params)}')

    strategy.max_profit()
    
    strategy.plot_payoff(35,55)