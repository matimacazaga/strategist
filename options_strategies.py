from options_base import Strategy, Put
import numpy as np 
from stocks_base import Stock

class CoveredPut(Strategy):

    def __init__(self, s0, strike):

        super().__init__('Covered Put')

        self.add_position([(-1, Stock(s0)), (-1, Put(strike))])

if __name__ == '__main__':

    s0 = 15.

    strategy = CoveredPut(s0, 12.)

    print(f'Pricing: {strategy.get_price(s0, 0.05, 0.15, 180, 1_000_000, 123)}')

    strategy.plot_payoff(8,15)