"""
Exotic Options - Single Asset 

Standard Barrier Options  

1. Formula
    A = fi * S * exp((b - r) * T) * N(fi * x1) - fi * X * exp(-r * T) * N(fi * x1 - fi * vol * sqrt(T))
    
    B = fi * S * exp((b - r) * T) * N(fi * x2) - fi * X * exp(-r * T) * N(fi * x2 - fi * vol * sqrt(T))
    
    C = fi * S * exp((b - r) * T) * (H / S)**2(u + 1) * N(ita * y1) - 
        fi * X * exp(-r * T) * (H / S)**2u * N(ita * y1 - ita * vol * sqrt(T))
    
    D = fi * S * exp((b - r) * T) * (H / S)**2(u + 1) * N(ita * y2) - 
        fi * X * exp(-r * T) * (H / S)**2u * N(ita * y2 - ita * vol * sqrt(T))
    
    E = K * exp(-r * T) * ( N(ita * x2 - ita * vol * sqrt(T)) - (H / S)**2u * N(ita * y2 - ita * vol * sqrt(T)) )
    
    F = K * ( (H / S)**(u + la) * N(ita * z) + (H / S)**(u - la) * N(ita * z - 2 * ita * la * vol * sqrt(T)) )

    where:
        x1 = log(S / X) / (vol * sqrt(T)) + (1 + u) * vol * sqrt(T)
        x2 = log(S / H) / (vol * sqrt(T)) + (1 + u) * vol * sqrt(T)
        y1 = log(H**2 / (S*X)) / (vol * sqrt(T)) + (1 + u) * vol * sqrt(T)
        y2 = log(H / S) / (vol * sqrt(T)) + (1 + u) * vol * sqrt(T)
        z  = log(H / S) / (vol * sqrt(T)) + la * vol * sqrt(T)
        u  = (b - vol**2 / 2) / vol**2
        la = sqrt(u**2 + 2*r / vol**2)
    
        K: a cash rebate which is paid at option expiration if the option has not come into existence or has become worthless
        H: barrier price
        ita, fi: parameters that is 1 or -1
        
2. Payoff
    "In" Barriers
    down-and-in call S > H
        ita = 1, fi = 1
    payoff = max(S - X, 0) if S <= H before T else K at expiration
        X > H: c = C + E
        X < H: c = A - B + D + E

    up-and-in call S < H
        ita = -1, fi = 1
    payoff = max(S - X, 0) if S >= H before T else K at expiration
        X > H: c = A + E
        X < H: c = B - C + D + E

    down-and-in put S > H
        ita = 1, fi = -1
    payoff = max(X - S, 0) if S <= H before T else K at expiration
        X > H: p = B - C + D + E
        X < H: p = A + E

    up-and-in put S < H
        ita = -1, fi = -1
    payoff = max(X - S, 0) if S >= H before T else K at expiration
        X > H: p = A - B + D + E
        X < H: p = C + E

    "Out" Barriers
    down-and-out call S > H
        ita = 1, fi = 1
    payoff = max(S - X, 0) if S > H before T else K at hit
        X > H: c = A - C + F
        X < H: c = B - D + F

    up-and-out call S < H
        ita = -1, fi = 1
    payoff = max(S - X, 0) if S >= H before T else K at hit
        X > H: c = F
        X < H: c = A - B + C - D + F

    down-and-out put S > H
        ita = 1, fi = -1
    payoff = max(X - S, 0) if S <= H before T else K at hit
        X > H: p = A - B + C - D + F
        X < H: p = F

    up-and-out put S < H
        ita = -1, fi = -1
    payoff = max(X - S, 0) if S >= H before T else K at hit
        X > H: p = B - D + F
        X < H: p = A - C + F
"""

from math import exp, log, sqrt

from options.functions import cdf
from options.option import OptionType


class BarrierType(object):
    IN = 0
    OUT = 1


class BarrierTypeError(Exception):
    def __str__(self):
        return 'Unknown barrier type. It must be BarrierType.IN or BarrierType.OUT'


class BarrierOption:
    
    def __init__(self, spot, strike, rate, expiry, vol, coc, rebate, bar):
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.expiry = expiry
        self.vol = vol
        self.coc = coc # b: cost of carry        
        self.rebate = rebate
        self.bar = bar

        self.u  = (coc - vol**2 / 2) / vol**2
        self.la = sqrt(self.u**2 + 2*rate / vol**2)
        self.z  = log(bar / spot) / (vol * sqrt(expiry)) + self.la * vol * sqrt(expiry)
        self.x1 = log(spot / strike) / (vol * sqrt(expiry)) + (1 + self.u) * vol * sqrt(expiry)
        self.x2 = log(spot / bar) / (vol * sqrt(expiry)) + (1 + self.u) * vol * sqrt(expiry)
        self.y1 = log(bar**2 / (spot*strike)) / (vol * sqrt(expiry)) + (1 + self.u) * vol * sqrt(expiry)
        self.y2 = log(bar / spot) / (vol * sqrt(expiry)) + (1 + self.u) * vol * sqrt(expiry)

    
    def _get_ABCDEF(self, ita, fi):

        A = fi * self.spot * exp((self.coc - self.rate) * self.expiry) * cdf(fi * self.x1) -    \
            fi * self.strike * exp(- self.rate * self.expiry) * cdf(fi * self.x1 - fi * self.vol * sqrt(self.expiry))
    
        B = fi * self.spot * exp((self.coc - self.rate) * self.expiry) * cdf(fi * self.x2) -    \
            fi * self.strike * exp(- self.rate * self.expiry) * cdf(fi * self.x2 - fi * self.vol * sqrt(self.expiry))
        
        C = fi * self.spot * exp((self.coc - self.rate) * self.expiry) * (self.bar / self.spot)**(2 * self.u + 2) * cdf(ita * self.y1) -    \
            fi * self.strike * exp(- self.rate * self.expiry) * (self.bar / self.spot)**(2 * self.u) * cdf(ita * self.y1 - ita * self.vol * sqrt(self.expiry))
        
        D = fi * self.spot * exp((self.coc - self.rate) * self.expiry) * (self.bar / self.spot)**(2 * self.u + 2) * cdf(ita * self.y2) -    \
            fi * self.strike * exp(- self.rate * self.expiry) * (self.bar / self.spot)**(2 * self.u) * cdf(ita * self.y2 - ita * self.vol * sqrt(self.expiry))
        
        E = self.rebate * exp(- self.rate * self.expiry) * ( cdf(ita * self.x2 - ita * self.vol * sqrt(self.expiry)) - 
                                                             (self.bar / self.spot)**(2 * self.u) * cdf(ita * self.y2 - ita * self.vol * sqrt(self.expiry)) )
        
        F = self.rebate * ( (self.bar / self.spot)**(self.u + self.la) * cdf(ita * self.z) + 
                            (self.bar / self.spot)**(self.u - self.la) * cdf(ita * self.z - 2 * ita * self.la * self.vol * sqrt(self.expiry)) )

        return A, B, C, D, E, F
        
    def get_payoff(self, opt_type, bar_type):
        
        if bar_type == BarrierType.IN:
            if opt_type == OptionType.CALL:
                if self.spot > self.bar: # down-and-in call
                    ita = 1
                    fi = 1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = C + E
                    else:
                        payoff = A - B + D + E
                else: # up-and-in call
                    ita = -1
                    fi = 1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = A + E
                    else:
                        payoff = B - C + D + E

            else:
                if self.spot > self.bar: # down-and-in put
                    ita = 1
                    fi = -1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = B - C + D + E
                    else:
                        payoff = A + E
                else: # up-and-in put
                    ita = -1
                    fi = -1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = A - B + D + E
                    else:
                        payoff = C + E

        elif bar_type == BarrierType.OUT:
            if opt_type == OptionType.CALL:
                if self.spot > self.bar: # down-and-out call
                    ita = 1
                    fi = 1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = A - C + F
                    else:
                        payoff = B - D + F
                else: # up-and-out call
                    ita = -1
                    fi = 1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = F
                    else:
                        payoff = A - B + C - D + F
            else:
                if self.spot > self.bar: # down-and-out put
                    ita = 1
                    fi = -1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = A - B + C - D + F
                    else:
                        payoff = F
                else: # up-and-out put
                    ita = -1
                    fi = -1
                    A, B, C, D, E, F = self._get_ABCDEF(ita, fi)
                    if self.strike > self.bar:
                        payoff = B - D + F
                    else:
                        payoff = A - C + F
        
        else:
            raise BarrierTypeError
        
        return round(payoff, 4)

        
if __name__ == '__main__':
    
    bo = BarrierOption(100, 90, 0.08, 0.5, 0.25, 0.04, 3, 95)
    assert bo.get_payoff(OptionType.CALL, BarrierType.OUT) == 9.0246
    assert bo.get_payoff(OptionType.PUT, BarrierType.OUT) == 2.2798
    assert bo.get_payoff(OptionType.CALL, BarrierType.IN) == 7.7627
    assert bo.get_payoff(OptionType.PUT, BarrierType.IN) == 2.9586

