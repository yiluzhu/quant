import matplotlib.pyplot as plt
import numpy as np
from options.option import OptionType, Option
from options.pricing.black_scholes import BlackScholesPricer


class OptionPricePlotter:
    def get_price(self, otype=OptionType.CALL, product='stock_option', 
                  spot=60, strike=65, rate=0.08, expiry=0.25, vol=0.3):
        """Q:  (Vanilla option)
            A European call option, 3 month to expiry, stock price is 60, the strike
            price is 65, risk free interest rate is 8% per year, volatility is 30% per year
        A:
            2.1334
        """
        option = Option(otype, spot, strike, rate, expiry, vol, product=product)
        pricer = BlackScholesPricer()
        return pricer.price_option(option)

    def plot_price_vs_expiry(self):
        months_to_expiry = np.arange(1, 800, 1)
        prices = [self.get_price(expiry=m * 1.0 / 12) for m in months_to_expiry]

        plt.plot(months_to_expiry, prices, # blue 
                 months_to_expiry, [60] * len(months_to_expiry), 'r--'  # red dash
                )
        plt.xlabel('Months to expiry')
        plt.ylabel('Option Price')
        plt.axis([0, 850, 0, 65])

    def plot_price_vs_strike(self):
        k_prices = np.arange(0.1, 90, 1)
        prices = [self.get_price(strike=k) for k in k_prices]

        plt.plot(k_prices, prices,
                 k_prices, [0] * len(k_prices), 'r--')
        plt.xlabel('Strike Price')
        plt.ylabel('Option Price')
        plt.axis([-10, 100, -10, 65])

    def plot_price_vs_spot(self):
        s_prices = np.arange(30, 90, 1)
        prices = [self.get_price(spot=s) for s in s_prices]

        plt.plot(s_prices, prices,
                 s_prices, [0] * len(s_prices), 'r--')
        plt.xlabel('Spot Price')
        plt.ylabel('Option Price')
        plt.axis([30, 90, -5, 30])

    def plot_price_vs_vol(self):
        """With volatility tends to infinity, 
        the price of option tends to spot price of underlying asset. 
        """
        vols = np.arange(0.1, 15, 0.1)
        prices = [self.get_price(vol=v) for v in vols]

        plt.plot(vols, prices,
                 vols, [60] * len(vols), 'r--')
        plt.xlabel('Volatility')
        plt.ylabel('Option Price')
        plt.axis([0, 15, 0, 65])


def get_bs_plot():
    bsptsp = OptionPricePlotter()
    
    fig = plt.figure(figsize =(8,12))
    
    plt.subplot(4, 1, 1)
    bsptsp.plot_price_vs_expiry()
    
    plt.subplot(4, 1, 2)
    bsptsp.plot_price_vs_strike()
    
    plt.subplot(4, 1, 3)
    bsptsp.plot_price_vs_spot()

    plt.subplot(4, 1, 4)
    bsptsp.plot_price_vs_vol()

    return fig


if __name__ == '__main__':
    fig = get_bs_plot()
    plt.show()