from options_base import Strategy, Put, Call
import numpy as np
from stocks_base import Stock
from utils import is_atm, is_otm, is_itm

class CoveredCall(Strategy):
    def __init__(self, initial_stock_price, strike):

        super().__init__('Covered Call')

        self.initial_stock_price = initial_stock_price

        self.add_position([(1, Stock(initial_stock_price)), (-1, Call(strike))])

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        max_profit = self.positions[1].get_strike() - self.initial_stock_price + C

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, C=None):

        if C is None:

            C = self.derivative_price

        max_loss = self.initial_stock_price - C

        print(f'Max Loss: {max_loss}')

        return max_loss

class CoveredPut(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Covered Put')

        self.initial_stock_price = initial_stock_price

        self.add_position([(-1, Stock(initial_stock_price)), (-1, Put(strike))])

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        max_profit = self.initial_stock_price - self.positions[1].get_strike() + C

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, C=None):

        max_loss = np.inf 

        print(f'Max Loss: {max_loss}')

        return max_loss 

class ProtectiveCall(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Protective Call')

        self.initial_stock_price = initial_stock_price

        delta_1 = 0.1 * initial_stock_price

        if not is_atm('Call', initial_stock_price, strike, delta_1) or not is_otm('Call', initial_stock_price, strike):

            raise ValueError('The call option must be ATM or OTM.')

        self.add_position([(-1, Stock(initial_stock_price)), (1, Call(strike))])

    def max_profit(self, D=None):

        if D is None:

            D = self.derivative_price

        max_profit = self.initial_stock_price - D

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        max_loss = self.positions[1].get_strike() - self.initial_stock_price + D

        print(f'Max Loss: {max_loss:.2f}')

        return max_loss

class ProtectivePut(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Protective Put')

        self.initial_stock_price = initial_stock_price

        delta_1 = 0.1 * initial_stock_price

        if not is_atm('Put', initial_stock_price, strike, delta_1) or not is_otm('Put', initial_stock_price, strike):

            raise ValueError('The put option must be ATM or OTM.')

        self.add_position([(1, Stock(initial_stock_price)), (1, Put(strike))])

    def max_profit(self, D=None):

        max_profit = np.inf 

        print(f'Max Profit: {max_profit}')

        return max_profit        

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        max_loss = self.initial_stock_price - self.positions[1].get_strike() + D

        print(f'Max Loss: {max_loss:.2f}')

        return max_loss

class BullPutSpread(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Bull Put Spread')

        if not is_otm('Put', initial_stock_price, strike_1):

            raise ValueError('The long option must be OTM.')

        if not is_otm('Put', initial_stock_price, strike_2):

            raise ValueError('The short option must be OTM.')

        if strike_2 < strike_1:

            raise ValueError('The strike price 2 must be greater than the strike price 1')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2))])

        self.initial_stock_price = initial_stock_price

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        print(f'Max Profit: {C:.2f}')

        return C

    def max_loss(self, C=None):

        if C is None:

            C = self.derivative_price

        max_loss = self.positions[0].get_strike() - self.positions[1].get_strike() - C

        print(f'Max Loss: {max_loss:.2f}')

        return max_loss

class BearPutSpread(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Bear Put Spread')

        self.initial_stock_price = initial_stock_price

        delta_1 = 0.1 * initial_stock_price

        if not is_atm('Put', initial_stock_price, strike_1, delta_1):

            raise ValueError('The long put must be ATM.')

        if not is_otm('Put', initial_stock_price, strike_2):

            raise ValueError('The short put must be OTM.')

        if strike_2 > strike_1:

            raise ValueError('The strike price 2 must be less than the strike price 1')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2))])

    def max_profit(self, D=None):

        if D is None:

            D = self.derivative_price

        max_profit = self.positions[0].get_strike() - self.positions[1].get_strike() - D

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        print(f'Max Loss: {D:.2f}')

        return D

class SyntheticShortForward(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Synthetic Short Forward')

        self.initial_stock_price = initial_stock_price

        if not is_atm('Put', initial_stock_price, strike):

            raise ValueError('Both the put and the call must be ATM.')

        self.add_position([(1, Put(strike)), (-1, Call(strike))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.initial_stock_price - H

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, H=None):

        max_loss = np.inf 

        print(f'Max Loss: {max_loss}')

        return max_loss 

class ShortRiskReversal(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Short Risk Reversal')

        self.initial_stock_price = initial_stock_price

        if not is_otm('Put', initial_stock_price, strike_1):

            raise ValueError('The put option must be OTM.')

        if not is_otm('Call', initial_stock_price, strike_2):

            raise ValueError('The call option must be OTM.')

        self.add_position([(1, Put(strike_1)), (-1, Call(strike_2))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.positions[0].get_strike() - H

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, H=None):

        max_loss = np.inf 

        print(f'Max Loss: {max_loss}')

        return max_loss

class BullPutLadder(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2, strike_3):

        super().__init__('Bull Put Ladder')

        self.initial_stock_price = initial_stock_price

        delta_1 = initial_stock_price * 0.1

        if not is_atm('Put', initial_stock_price, strike_1, delta_1):
            
            raise ValueError('The strike price of the'
                             'short put must be close to the initial stock price (ATM).')

        if not is_otm('Put', initial_stock_price, strike_2):

            raise ValueError('The first long put option must be OTM.')

        if not is_otm('Put', initial_stock_price, strike_3):

            raise ValueError('The second long put option must be OTM.')

        self.add_position([(-1, Put(strike_1)), (1, Put(strike_2)), (1, Put(strike_3))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.positions[2].get_strike() + self.positions[1].get_strike() - self.positions[0].get_strike() - H 

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit

    def max_loss(self, H=None):

        if H is None:

            H = self.derivative_price

        max_loss = self.positions[0].get_strike() - self.positions[1].get_strike() + H 

        print(f'Max Loss: {max_loss:.2f}')

        return max_loss

class BearPutLadder(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2, strike_3):

        super().__init__('Bear Put Ladder')

        self.initial_stock_price = initial_stock_price

        delta_1 = initial_stock_price * 0.1 

        if not is_atm('Put', initial_stock_price, strike_1, delta_1):

            raise ValueError('The strike price of the'
                             'long put must be close to the initial stock price (ATM).')

        if not is_otm('Put', initial_stock_price, strike_2): 

            raise ValueError('The first short put option must be OTM.')

        if not is_otm('Put', initial_stock_price, strike_3):

            raise ValueError('The second short put option must be OTM.')

        self.add_position([(1, Put(strike_1)), (-1, Put(strike_2)), (-1, Put(strike_3))])

    def max_profit(self, H=None):

        if H is None:

            H = self.derivative_price

        max_profit = self.positions[0].get_strike() - self.positions[1].get_strike() - H

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit 

    def max_loss(self, H=None):

        if H is None:

            H = self.derivative_price 

        max_loss = self.positions[2].get_strike() + self.positions[1].get_strike() - self.positions[0].get_strike() + H 

        print(f'Max Loss: {max_loss:.2f}') 

        return max_loss

class LongStrangle(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Long Strangle')

        self.initial_stock_price = initial_stock_price

        if not is_otm('Call', initial_stock_price, strike_1):

            raise ValueError('The long call must be OTM.')

        if not is_otm('Put', initial_stock_price, strike_2):

            raise ValueError('The long put must be OTM.')

        self.add_position([(1, Call(strike_1)), (1, Call(strike_2))])

    def max_profit(self, D=None):

        max_profit = np.inf

        print(f'Max Profit: {max_profit}')

        return max_profit

    def max_loss(self, D=None):

        if D is None:

            D = self.derivative_price

        print(f'Max Loss: {D:.2f}')

        return D 

class ShortStraddle(Strategy):

    def __init__(self, initial_stock_price, strike):

        super().__init__('Short Straddle')

        self.initial_stock_price = initial_stock_price

        if not is_atm('Call', initial_stock_price, strike):

            raise ValueError('Both the call and the put must be ATM.')

        self.add_position([(-1, Call(strike)), (-1, Put(strike))])

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        print(f'Max Profit: {C:.2f}')

        return C 

    def max_loss(self, C=None):

        max_loss = np.inf 

        print(f'Max Loss: {max_loss}')

        return max_loss    

class ShortGuts(Strategy):

    def __init__(self, initial_stock_price, strike_1, strike_2):

        super().__init__('Short Guts')

        self.initial_stock_price = initial_stock_price

        if not is_itm('Call', initial_stock_price, strike_1):

            raise ValueError('The short call must be ITM.')

        if not is_itm('Put', initial_stock_price, strike_2):

            raise ValueError('The short put must be ITM.')

        self.add_position([(-1, Call(strike_1)), (-1, Put(strike_2))])

    def max_profit(self, C=None):

        if C is None:

            C = self.derivative_price

        max_profit = C - (self.positions[1].get_strike() - self.positions[0].get_strike())

        print(f'Max Profit: {max_profit:.2f}')

        return max_profit 

    def max_loss(self, C=None):

        max_loss = np.inf 

        print(f'Max Loss: {max_loss}')

        return max_loss  

if __name__ == '__main__':

    #initial_stock_price = 275.
    initial_stock_price = 60.

    #strategy = SyntheticShortForward(initial_stock_price)
    strategy = BullPutLadder(initial_stock_price, 61., 55., 53.)

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

