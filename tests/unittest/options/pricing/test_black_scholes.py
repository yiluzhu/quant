from unittest import TestCase

from options.option import OptionType, Option
from options.pricing.black_scholes import BlackScholesPricer


class BlackScholesModelTestCase(TestCase):

    def setUp(self):
        self.pricer = BlackScholesPricer()

    def test_vanilla_call_option(self):
        """
        Q:  (Vanilla option)
            A European call option, 3 month to expiry, stock price is 60, the strike
            price is 65, risk free interest rate is 8% per year, volatility is 30% per year
        A:
            the option price should be 2.1334
        """
        option = Option(OptionType.CALL, 60, 65, 0.08, 0.25, 0.3, product='stock_option')
        result = self.pricer.price_option(option)
        self.assertEqual(2.1334, result)

    def test_vanilla_option_with_dividend(self):
        """
        Q:  (Vanilla option with yield)
            A European put option, 6 month to expiry, stock price is 100, the strike
            price is 95, risk free interest rate is 10% per year, 
            the dividend is 5% per year, volatility is 20% per year
        A:
            2.4648
        """
        option = Option(OptionType.PUT, 100, 95, 0.1, 0.5, 0.2, dividend=0.05, product='stock_option_with_dividend')
        result = self.pricer.price_option(option)
        self.assertEqual(2.4648, result)

    def test_options_on_futures(self):
        """ 
        Q:  (Options on Futures)
            A European option on futures, 9 month to expiry, future price is 19, the strike
            price is 19, risk free interest rate is 10% per year, volatility is 28% per year
            dividend is 10% per year
        A:
            c = p = 1.7011
        """
        option1 = Option(OptionType.CALL, 19, 19, 0.1, 0.75, 0.28, dividend=0.1, product='futures_option')
        result1 = self.pricer.price_option(option1)
        self.assertEqual(1.7011, result1)
        option2 = Option(OptionType.PUT, 19, 19, 0.1, 0.75, 0.28, dividend=0.1, product='futures_option')
        result2 = self.pricer.price_option(option2)
        self.assertEqual(1.7011, result2)

    def test_options_on_FX(self):
        """ 
        Q:  (Options on FX)
            A European USD-call/EUR-put option, 6 month to expiry, USD/EUR exchange rate is 1.56, 
            the strike exchange rate is 1.6, the domestic risk free interest rate in EUR is 8% per year, 
            the foreign risk-free interest rate in USD is 6%, volatility is 12% per year
        A:
            c = 0.0291
        """
        option1 = Option(OptionType.CALL, 1.56, 1.6, 0.06, 0.5, 0.12, dividend=0.08, product='currency_option')
        result1 = self.pricer.price_option(option1)
        self.assertEqual(0.0291, result1)

        option2 = Option(OptionType.PUT, 1/1.56, 1/1.6, 0.08, 0.5, 0.12, dividend=0.06, product='currency_option')
        result2 = self.pricer.price_option(option2)
        self.assertEqual(0.0117, result2)

        #self.assertEqual(0.0291 / 1.56, # Percentage of EUR
        #                 0.0117 * 1.6)  # Percentage of USD

    def test_compare_binomial_tree(self):
        """
        European put option, 2 years to expiry, spot price 50, strike price 52, risk free rate 5%,
        volatility 30%
        
        The result from binomial trees with steps == 10 : 6.747
                                                     100: 6.7781
                                                     500: 6.7569
        """
        option = Option(OptionType.PUT, 50, 52, 0.05, 2, 0.3, product='stock_option')
        result = self.pricer.price_option(option)
        self.assertEqual(6.7601, result)
