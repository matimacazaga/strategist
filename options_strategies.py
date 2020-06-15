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

    def max_profit(self, D=None):

        if D is None:

            D = self.derivative_price

        max_profit = self.initial_stock_price - D 

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        max_loss = self.positions[1][1].strike - self.initial_stock_price + D    

        print(f'Max Loss: {max_loss:.2f}')

class BullPutSpread(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Bull Put Spread')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price
        
        return C 

    def max_loss(self, C=None):

        if C is None:

            C = self.derivative_price 

        return self.positions[0][1].strike - self.positions[1][1].strike - C 

if __name__ == '__main__':

    initial_stock_price = 275.
    #initial_stock_price = 50.

    strategy = BullPutSpread(initial_stock_price, 270., 280.)
    #strategy = ProtectiveCall(initial_stock_price, 55.)

    params = {'risk_free': 0.05, 'sigma': 0.15,
              'plazo': 30, 'n': 1_000_000, 
              'seed': 123}
    #params = {'risk_free': 0.05, 'sigma':0.15, 
    #          'plazo': 180, 'n':1_000_000,
    #          'seed': 123}

    print(f'Pricing: {strategy.get_price(**params)}')

    #print(f'Pricing: {strategy.get_price(**params)}')

    strategy.max_profit()

    strategy.max_loss()
    
    strategy.plot_payoff(200, 300)

