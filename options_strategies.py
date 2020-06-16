from options_base import Strategy, Put, Call
import numpy as np
from stocks_base import Stock


class CoveredCall(Strategy):
    def __init__(self, initial_stock_price, strike):

        super().__init__('Covered Call')

        self.add_position([(1, Stock(initial_stock_price)), (-1, Call(strike))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        max_profit = self.positions[1].get_strike() - self.initial_stock_price + C

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self, C=None):

        if C is None:

            C = self.derivative_price

        max_loss = self.initial_stock_price - C

        print(f'Max Loss: {max_loss}')


class CoveredPut(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Covered Put')

        self.add_position([(-1, Stock(initial_stock_price)), (-1, Put(strike))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        max_profit = self.initial_stock_price - self.positions[1].get_strike() + C

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self):

        print(f'Max Loss: {np.inf}')


class ProtectiveCall(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Protective Call')

        if strike > initial_stock_price:

            raise ValueError('The call option must be ATM or OTM.')

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

        max_loss = self.positions[1].get_strike() - self.initial_stock_price + D

        print(f'Max Loss: {max_loss:.2f}')

class ProtectivePut(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Protective Put')

        if strike < initial_stock_price:

            raise ValueError('The Put option must be ATM or OTM.')

        self.add_position([(1, Stock(initial_stock_price)), (1, Put(strike))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self):

        print(f'Max Profit: {np.inf}')

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        max_loss = self.initial_stock_price - self.positions[1].get_strike() + D

        print(f'Max Loss: {max_loss:.2f}')


class BullPutSpread(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Bull Put Spread')

        if strike_1 >= initial_stock_price:

            raise ValueError('The long option must be OTM.')

        if strike_2 >= initial_stock_price:

            raise ValueError('The short option must be OTM.')

        if strike_2 < strike_1:
            raise ValueError('The strike price 2 must be greater than the strike price 1')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        print(f'Max Profit: {C:.2f}')

    def max_loss(self, C=None):

        if C is None:

            C = self.derivative_price

        max_loss = self.positions[0].get_strike() - self.positions[1].get_strike() - C

        print(f'Max Loss: {max_loss:.2f}')

class BearPutSpread(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Bear Put Spread')

        self.initial_stock_price = initial_stock_price

        if strike_1 != initial_stock_price:

            raise ValueError('The long put must be ATM.')

        if strike_2 >= initial_stock_price:

            raise ValueError('The short put must be OTM.')

        if strike_2 > strike_1:

            raise ValueError('The strike price 2 must be less than the strike price 1')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2))])

    def max_profit(self, D=None):

        if D is None:

            D = self.derivative_price

        max_profit = self.positions[0].get_strike() - self.positions[1].get_strike() - D

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        print(f'Max Loss: {D:.2f}')

class SyntheticShortForward(Strategy):

    def __init__(self, initial_stock_price):

        super().__init__('Synthetic Short Forward')

        self.initial_stock_price = initial_stock_price

        self.add_position([(1, Put(initial_stock_price)), (-1, Call(initial_stock_price))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.initial_stock_price - H

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self, H=None):

        print(f'Max Loss: {np.inf}')

class ShortRiskReversal(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Short Risk Reversal')

        if strike_1 > initial_stock_price:

            raise ValueError('The put option must be OTM.')

        if strike_2 < initial_stock_price:

            raise ValueError('The call option must be OTM.')

        self.add_position([(1, Put(strike_1)), (-1, Call(strike_2))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.positions[0].get_strike() - H

        print(f'Max Profit: {max_profit:.2f}')

    def max_loss(self, H=None):

        print(f'Max Loss: {np.inf}')

if __name__ == '__main__':

    #initial_stock_price = 275.
    initial_stock_price = 60.

    #strategy = SyntheticShortForward(initial_stock_price)
    strategy = ProtectiveCall(initial_stock_price, 55.)

    #params = {'risk_free': 0.05, 'sigma': 0.15,
    #          'plazo': 30, 'n': 1_000_000,
    #          'seed': 123}
    params = {'risk_free': 0.05, 'sigma':0.15,
              'plazo': 180, 'n':1_000_000,
              'seed': 123}

    print(f'Pricing: {strategy.get_price(**params)}')

    strategy.max_profit()

    strategy.max_loss()

    strategy.plot_payoff(0., initial_stock_price + 10)

