from unittest import TestCase

from options.option import OptionType
from options.pricing.barrier_options import BarrierOption, BarrierType


class BarrierOptionsTestCase(TestCase):
    
    def test_all(self):
        ''' from Option Pricing Formulas page 154 table 4-13
        S = 100, K = 3, T = 0.5, r = 0.08, b = 0.04'''
        spot = 100 
        rebate = 3
        rate = 0.08 
        expiry = 0.5
        vol = 0.25
        coc = 0.04

        opt_types = (OptionType.CALL, OptionType.PUT)
        bar_types = (BarrierType.OUT, BarrierType.IN)
        strikes = (90, 100, 110)
        bars = (95, 100, 105)

        values = (9.0246, 6.7924, 4.8759, 3.0, 3.0, 3.0, 2.6789, 2.3580, 2.3453,            # down-and-out call
                  7.7627, 4.0109, 2.0576, 13.8333, 7.8494, 3.9795, 14.1112, 8.4482, 4.5910, # down-and-in  call
                  2.2798, 2.2947, 2.6252, 3.0, 3.0, 3.0, 3.7760, 5.4932, 7.5187,            # down-and-out put
                  2.9586, 6.5677, 11.9752, 2.2845, 5.9085, 11.6465, 1.4653, 3.3721, 7.0846, # down-and-in  put
                 )
        
        i = 0
        for otype in opt_types:
            for btype in bar_types:
                for bar in bars:
                    for strike in strikes:
                        bo = BarrierOption(spot, strike, rate, expiry, vol, coc, rebate, bar)
                        self.assertEqual(bo.get_payoff(otype, btype), values[i])
                        i += 1
