from unittest import TestCase

from options.black_scholes_greeks import BlackScholesGreeks
from options.option import OptionType, Option
from options.pricing.black_scholes import BlackScholesPricer


class BlackScholesGreeksTestCase(TestCase):
    def test_delta_greeks(self):
        """
        Q:  (Delta Greeks)
            A future option, 6 month to expiry, the futures price is 105, 
            the strike strike price is 100, risk free interest rate is 10% per year, 
            volatility is 36% per year
        A:
            delta_call = 0.5946
            delta_put = -0.3566
        """
        option1 = Option(OptionType.CALL, 105, 100, 0.1, 0.5, 0.36, product='futures_option')
        bsg1 = BlackScholesGreeks(option1)
        self.assertEqual(0.5946,
                         bsg1.get_delta_greeks())

        option2 = Option(OptionType.PUT, 105, 100, 0.1, 0.5, 0.36, product='futures_option')
        bsg2 = BlackScholesGreeks(option2)
        self.assertEqual(-0.3566,
                         bsg2.get_delta_greeks())

    def test_delta_greeks2(self):
        """
        Q:
            A commodity option with two years to expiration. The commodity price
            is 90, the strike price is 40, the risk-free interest rate is 3% per year,
            the cost-of-carry is 9% per year, and the volatility is 20%. 
            What's the delta of a call option?
        A:
            delta_call = 1.1273
            This implies that the call option price will increase/decrease 1.1273 USD
            if the spot price increase/decrease by 1 USD
        """
        option = Option(OptionType.CALL, 90, 40, 0.03, 2, 0.2, cost_of_carry=0.09)
        bsg = BlackScholesGreeks(option)
        self.assertEqual(1.1273,
                         bsg.get_delta_greeks())

        # For every 1 dollar increase/decrease of the spot price, the option price increase/decrease 1.1273
        option = Option(OptionType.CALL, 90, 40, 0.03, 2, 0.2, cost_of_carry=0.09)
        pricer = BlackScholesPricer()
        opt_price = pricer.price_option(option)

        self.assertAlmostEqual(opt_price + 1.1273,
                               pricer.price_option(Option(OptionType.CALL, 91, 40, 0.03, 2, 0.2, cost_of_carry=0.09)),
                               3)
        self.assertEqual(round(opt_price - 1.1273, 4),
                         pricer.price_option(Option(OptionType.CALL, 89, 40, 0.03, 2, 0.2, cost_of_carry=0.09)))
