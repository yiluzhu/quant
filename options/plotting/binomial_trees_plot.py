from math import ceil
from multiprocessing import Process, Queue

import matplotlib.pyplot as plt
from options.pricing.binomial_trees import BinomialTreePricer
from options.option import OptionType, Option


class OptionPricePlotter:
    def __init__(self, otype=OptionType.PUT, spot=50,
                 strike=52, rate=0.05, expiry=2, vol=0.3, steps=1):
        self.option = Option(otype, spot, strike, rate, expiry, vol)
        self.pricer = BinomialTreePricer(steps)

    def get_price(self, steps):
        """European option, spot price 50, strike price 52, 
        risk free interest rate 5%, expiry 2 years, volatility 30%
        """
        self.pricer.set_steps(steps)
        return self.pricer.price_option(self.option)

    def _ps_slice(self, steps_list_slice, resultq, idx):
        prices = [self.get_price(steps=steps) for steps in steps_list_slice]
        resultq.put((idx, prices))
        resultq.close()

    def plot_price_vs_steps(self, start, end, step, ps_num=16):
        """ps_num: run in multiprocess mode with ps_num processes
        To run in single process mode, ps_num = 0
        """
        steps_list = range(start, end, step)

        if ps_num:
            # Multi processing
            resultq = Queue()
            slice_len = int(ceil(len(steps_list) * 1.0 / ps_num))
            processes = [Process(target=self._ps_slice, args=(steps_list[i*slice_len : (i+1)*slice_len], resultq, i)) for i in range(ps_num)]
            for p in processes:
                p.start()
            for p in processes:
                p.join()
            
            # Make sure to concatenate lists in order
            dict = {}
            while not resultq.empty():
                key, value = resultq.get()
                dict[key] = value
            
            prices = []
            for k in sorted(dict.keys()):
                prices += dict[k]
                
        else:
            # Single processing
            prices = [self.get_price(steps=steps) for steps in steps_list]

        fig = plt.figure()
        plt.plot(steps_list, prices)

        plt.xlabel('Number of steps for Binomial Tree')
        plt.ylabel('Option Price')
        #plt.axis([0, 300, 6, 8])
        print(prices[-1])
        return fig


def get_bt_plot():
    opp = OptionPricePlotter()
    # plt.subplot(2, 1, 1)
    # opp.plot_price_vs_steps(2, 50, 1)

    # plt.subplot(2, 1, 2)
    # opp.plot_price_vs_steps(200, 300, 3)
    import time
    t0 = time.time()
    fig = opp.plot_price_vs_steps(6, 300, 1, 4)
    # (6, 900, 3): M5: 90  M10: 77  M20: 65  M30: 77  S: 171
    # (6, 400, 1): S: 42
    # (6, 300, 1): S: 18  M4: 13  M10: 14
    return fig


if __name__ == '__main__':
    fig = get_bt_plot()
    fig.show()
