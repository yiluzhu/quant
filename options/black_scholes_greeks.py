"""
Delta: changes in the underlying asset price

    delta_call = exp((b - r) * T) * N(d1)         > 0
    delta_put  = exp((b - r) * T) * (N(d1) - 1)   < 0
    
    where 
        b: is cost of carry
        r: risk free interest rate
"""

from math import exp

from options.functions import cdf
from options.option import OptionType
from options.pricing.black_scholes import BlackScholesPricer


class BlackScholesGreeks:
    def __init__(self, option):
        self.pricer = BlackScholesPricer()
        self.option = option
    
    def get_delta_greeks(self, round_digit=4):
        d1 = self.pricer.get_d1_d2(self.option.spot, self.option.strike, self.option.expiry, self.option.vol, self.option.cost_of_carry)[0]
        if self.option.type == OptionType.CALL:
            delta = exp((self.option.cost_of_carry - self.option.rate) * self.option.expiry) * cdf(d1)
        else:
            delta = exp((self.option.cost_of_carry - self.option.rate) * self.option.expiry) * (cdf(d1) - 1)

        return round(delta, round_digit)
