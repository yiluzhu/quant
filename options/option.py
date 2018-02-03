from enum import Enum


class Option:
    """One option object"""
    def __init__(self, type, spot, strike, rate, expiry, vol, dividend=0, cost_of_carry=0, product=''):
        self.type = type
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.expiry = expiry
        self.vol = vol
        self.dividend = dividend
        self.cost_of_carry = cost_of_carry
        self.product = product

        product_coc_map = {
            'stock_option': rate,
            'stock_option_with_dividend': rate - dividend,
            'futures_option': 0,
            'margined_futures_option': 0,
            'currency_option': rate - dividend,
        }
        if not self.cost_of_carry and product in product_coc_map:
            self.cost_of_carry = product_coc_map[product]


class OptionType(Enum):
    CALL = 0
    PUT = 1


class OptionTypeError(Exception):
    def __str__(self):
        return 'Unknown option type. It must be OptionType.CALL or OptionType.PUT'


