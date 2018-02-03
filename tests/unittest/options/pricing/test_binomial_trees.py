
from unittest import TestCase

from options.pricing.binomial_trees import BinomialTreePricer
from options.option import OptionType, Option


class BinomialTreeTestCase(TestCase):

    def test_basic(self):
        """European option, spot price 50, strike price 52, risk free interest rate 5%
        expiry 2 years, volatility 30%
        """
        pricer = BinomialTreePricer(steps=100)
        option = Option(OptionType.PUT, 50, 52, 0.05, 2, 0.3)
        result = pricer.price_option(option)
        self.assertEqual(6.7781, result)
