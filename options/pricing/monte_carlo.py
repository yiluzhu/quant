"""
For each path of simulation, the final price is:

    St = spot * exp((b - vol*vol/2) * T + vol * rand * sqrt(T))
    where rand is a random number in (0, 1)

    call option:
        each_price = max(St - strike, 0)
    put option:
        each_price = max(strike - St, 0)

The overall price is:
    sum(each_price) * exp(rate * T) / simu_num
"""

from math import exp, sqrt
from multiprocessing import Process, Queue
from random import random

from options.functions import norminv
from options.option import OptionType


# from scipy.stats import norm   # norm.ppf is about 50 times slower than norminv but no obvious accuracy improvement


class MonteCarloPricer:
    def __init__(self, simu_num=1000000, ps_num=10):
        self.simu_num = simu_num
        self.ps_num = ps_num

    def set_ps_num(self, ps_num):
        self.ps_num = ps_num

    def get_price_of_one_run(self, z):
        '''Run the simulation once and return the option price'''
        #st = self.spot * exp((self.cost_of_carry - self.vol**2 / 2) * self.expiry + self.vol * norm.ppf(random()) * sqrt(self.expiry))
        st = self.spot * exp((self.cost_of_carry - self.vol**2 / 2) * self.expiry + self.vol * norminv(random()) * sqrt(self.expiry))
        return max(z * (st - self.strike), 0)

    def _ps_slice(self, z, num, resultq):
        sum = 0
        for i in range(int(num)):
            sum += self.get_price_of_one_run(z)

        resultq.put(sum)
        resultq.close()

    def price_option(self, option):
        """
        simu_num: the number of simulation runs, usually > 100000
        ps_num: If zero, run simulation in single process mode;
                otherwise run in multiprocess mode with ps_num processes to speed up
        """
        self.spot = option.spot
        self.strike = option.strike
        self.rate = option.rate
        self.expiry = option.expiry
        self.vol = option.vol
        self.cost_of_carry = option.cost_of_carry or option.rate

        z = 1 if option.type == OptionType.CALL else -1

        sum = 0
        if self.ps_num:
            # multiprocess mode
            if (self.simu_num / self.ps_num <= 1000): # when > 1000, simu_num / ps_num ~= simu_num / ps_num +- simu_num % ps_num
                assert not self.simu_num % self.ps_num, \
                    'simu_num must be integer times of ps_num; received simu_num: {}, ps_num: {}'.format(self.simu_num, self.ps_num)
            resultq = Queue()
            processes = [Process(target=self._ps_slice, args=(z, self.simu_num / self.ps_num, resultq)) for i in range(self.ps_num)]
            for p in processes:
                p.start()
            for p in processes:
                p.join()

            while not resultq.empty():
                sum += resultq.get()

        else:
            # single process mode
            for i in range(self.simu_num):
                sum += self.get_price_of_one_run(z)

        return round(exp(- self.rate * self.expiry) * sum / self.simu_num, 4)
