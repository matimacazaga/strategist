import numpy as np 
from abc import ABC, abstractmethod

class Stock(ABC):

    def __init__(self, s0):

        self.__s0 = s0

        self.type = 'Stock'

    @staticmethod
    def sim_gbm(s0, drift, sigma, plazo, n=None):

        if n is None:
            n = 1

        st = s0 * np.exp((drift - .5 * sigma**2) * (plazo / 365.) + 
            sigma * np.sqrt(plazo / 365.) * np.random.normal(size=n))
        
        return st 

    def payoff(self, st):

        return st - self.__s0 
    

    