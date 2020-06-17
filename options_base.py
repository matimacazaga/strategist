from abc import ABC, abstractmethod
import numpy as np 
from stocks_base import Stock
import matplotlib.pyplot as plt 

plt.style.use('ggplot')

class EuroDerivative(ABC):

    def __init__(self, initial_stock_price=None):

        self._initial_stock_price = initial_stock_price

        self._derivative_price = None

    @property 
    def initial_stock_price(self):

        return self._initial_stock_price 

    @initial_stock_price.setter
    def initial_stock_price(self, value):

        if value < 0.:
            raise ValueError('Initial stock price cannot be less than 0.')

        self._initial_stock_price = value

    @property
    def derivative_price(self):

        if self._derivative_price is None: 

            raise ValueError('You should first get the price of the '
                             'strategy for a given set of parameters '
                             'or provide a value.')

        return self._derivative_price

    @derivative_price.setter 
    def derivative_price(self, value):

        self._derivative_price = value 

    def get_price(self, risk_free, sigma, plazo, n, initial_stock_price=None, seed=None):

        if initial_stock_price:

            self.initial_stock_price = initial_stock_price

        if seed:
            np.random.seed(seed)

        self.derivative_price = np.abs(np.mean(self.payoff(Stock.sim_gbm(self.initial_stock_price, risk_free, sigma, plazo, n))))
        
        return self.derivative_price 

    @abstractmethod
    def payoff(self, st):
        """
        Computa el payoff de la opción.

        Argumentos
        ----------
        st: float
            Precio final del subyacente.
        
        Retorno
        -------
        p: float
            Payoff de la opción para un dado st.
        """
        pass

    def plot_payoff(self, min_val, max_val):

        price_range = np.arange(min_val, max_val, 0.01)

        fig, ax = plt.subplots(figsize=(12,8))

        ax.plot(price_range, self.payoff(price_range))

        ax.set_xlabel('$S_{t}$', fontsize=14)

        ax.set_ylabel('Payoff', fontsize=14)

        return fig, ax

class VanillaOption(EuroDerivative):

    def __init__(self, option_type, strike):

        super().__init__()
        
        self.type = option_type 

        self.strike = strike 
    
    def __repr__(self,):
        
        return f'{self.type} @ {self.strike:.2f}'


class Call(VanillaOption):

    def __init__(self, strike):
        
        super().__init__('Call', strike)

    def payoff(self, st):

        return np.maximum(0., st - self.strike)

class Put(VanillaOption):

    def __init__(self, strike):

        super().__init__('Put', strike)

    def payoff(self, st):

        return np.maximum(0., self.strike - st)

class Position:

    def __init__(self, quantity, instrument):

        self.__quantity = quantity

        self.__instrument = instrument 

    @property
    def quantity(self):

        return self.__quantity 

    @quantity.setter
    def quantity(self, value):
        if isinstance(value, int):
            self.__quantity = value
        else:
            raise ValueError('Quantity must be an integer') 

    @property
    def instrument(self):

        return self.__instrument 
    
    @instrument.setter
    def intrument(self, instrument):

        self.__instrument = instrument 

    def get_type(self):

        return self.instrument.type 

    def get_strike(self):

        if hasattr(self.__instrument, 'strike'):

            return self.__instrument.strike 
        
        else:

            raise AttributeError('The selected instrument hasn\'t got a strike price.')
        
class Strategy(EuroDerivative):

    def __init__(self, name):

        super().__init__()

        self._strategy_name = name 

        self._positions = []

    @property 
    def strategy_name(self):

        return self._strategy_name 

    @property 
    def positions(self):

        return self._positions 

    def __repr__(self):

        output_title = [f'Strategy: {self.strategy_name}', 20*'-']

        pos_string = [f'{"Long " if pos.quantity > 0 else "Short "}' + 
                      f'{abs(pos.quantity)} {pos.get_type()} @ ' + 
                      f'{pos.get_strike():.2f}' for pos in self.positions]

        end_line = [20*'-']

        string_to_print = output_title + pos_string + end_line 

        return '\n'.join(string_to_print)

    def add_position(self, positions):

        if isinstance(positions, list):
            for q,i in positions:

                self._positions.append(Position(q,i))

        else:
            raise TypeError('The positions argument must be a list')
        """
        if isinstance(pos, list) or isinstance(pos, tuple):
            self._positions.extend(pos)

        else:
            self._positions.append(pos)
        """
    def payoff(self, st):

        payoffs = np.sum(np.array([pos.quantity * pos.instrument.payoff(st) for pos in self.positions]),axis=0)
        
        return payoffs

    def plot_payoff(self, min_val, max_val):
 
        _, ax = super().plot_payoff(min_val, max_val)

        ax.set_title(self.strategy_name, fontsize=16)

        plt.show()

if __name__ == '__main__':

    positions = []

    for q,i in [(1, Call(10.))]:

        positions.append(Position(q,i))

    print(positions[0].get_strike())

    strategy = Strategy('Butterfly')

    positions = [(1, Call(14.)), (1, Call(10.)), (-2, Call(12.))]

    strategy.add_position(positions)

    print(strategy)

    params = {'risk_free': 0.05, 'sigma':0.15, 
               'plazo': 180, 'n':1_000_000, 'initial_stock_price': 10, 'seed': 123}

    print(f'Pricing: {strategy.get_price(**params)}')

    strategy.plot_payoff(8,15)