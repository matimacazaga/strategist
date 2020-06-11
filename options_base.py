from abc import ABC, abstractmethod
import numpy as np 
from stocks_base import Stock
import matplotlib.pyplot as plt 

plt.style.use('ggplot')

class EuroDerivative(ABC):

    def get_price(self, s0, risk_free, sigma, plazo, n, seed=None):

        if seed:
            np.random.seed(seed)

        return np.mean(self.payoff(Stock.sim_gbm(s0, risk_free, sigma, plazo, n)))

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

class Strategy(EuroDerivative):

    def __init__(self, name):

        self.__strategy_name = name 

        self.__positions = []

    def __repr__(self):

        output_title = [f'Strategy: {self.__strategy_name}', 20*'-']

        pos_string = [f'{"Long " if pos[0] > 0 else "Short "}' + 
                      f'{abs(pos[0])} {pos[1].type} @ ' + 
                      f'{pos[1].strike:.2f}' for pos in self.__positions]

        end_line = [20*'-']

        string_to_print = output_title + pos_string + end_line 

        return '\n'.join(string_to_print)

    def add_position(self, pos):

        if isinstance(pos, list) or isinstance(pos, tuple):
            self.__positions.extend(pos)

        else:
            self.__positions.append(pos)

    def payoff(self, st):
        payoffs = np.sum(np.array([q * o.payoff(st) for q, o in self.__positions]),axis=0)
        return payoffs

    def plot_payoff(self, min_val, max_val):

        fig, ax = super().plot_payoff(min_val, max_val)

        ax.set_title(self.__strategy_name, fontsize=16)

        plt.show()

if __name__ == '__main__':

    strategy = Strategy('Butterfly')

    positions = [(1, Call(14.)), (1, Call(10.)), (-2, Call(12.))]

    strategy.add_position(positions)

    print(strategy)

    print(f'Pricing: {strategy.get_price(10., 0.05, 0.15, 180, 1_000_000, 123)}')

    strategy.plot_payoff(8,15)