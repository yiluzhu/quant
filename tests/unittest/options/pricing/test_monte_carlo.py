import time
from unittest import TestCase

from options.option import OptionType, Option
from options.pricing.monte_carlo import MonteCarloPricer


class MonteCarloTestCase(TestCase):
    
    def setUp(self):
        self.pricer = MonteCarloPricer(300000)
        self.t0 = time.time()

    def test_eu_call_opt(self):
        """2-year European put option, spot price 50, strike 52
        risk-free rate 5%, volatility 30%
        """
        option = Option(OptionType.PUT, 50, 52, 0.05, 2, 0.3)
        self.pricer.set_ps_num(0)  # single process
        result = self.pricer.price_option(option)
        self.assertAlmostEqual(6.7601, result, 1)

    def test_eu_call_opt_with_mp(self):
        """Run the same test but in multiprocess mode
        """
        option = Option(OptionType.PUT, 50, 52, 0.05, 2, 0.3)
        self.pricer.set_ps_num(4)  # single process
        result = self.pricer.price_option(option)
        self.assertAlmostEqual(6.7601, result, 1)

    def tearDown(self):
        print('{} takes {} seconds'.format(self.__str__(), time.time() - self.t0))
