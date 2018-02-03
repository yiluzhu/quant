"""
Calculate option price using Binomial trees:

    u = exp(vol * sqrt(delta_t))    1 < u < 2
    d = 2 - u    
        when steps is very big, it's approximately equal to 1 / u 

    p = (a - d) / (u - d)
    
    where 
        a = exp(rate * delta_t)
        delta_t = expiry / steps
        p: the probability of an up movement in a risk neutral world 
        u: how much the price move up.      e.g. u=1.2 means the price will be 1.2 * spot   
        d: how much the price move down.    e.g. d=0.8 means the price will be 0.8 * spot
        
        
if for step N the value of option is x(up) and y(down), 
then for previous step N - 1 the value of option is:
    (x * p + y * (1 - p)) / a
        
        
Note:
    As we assume there is no arbitrage oppotunities, option value is the same as option price
"""

from math import sqrt, exp

from options.option import OptionType


class BinomialTreePricer:
    def __init__(self, steps=30):
        assert type(steps) == int and steps > 0, 'Type and value of steps are {} {}'.format(type(steps), steps)
        self.steps = steps

    def set_steps(self, steps):
        assert type(steps) == int and steps > 0, 'Type and value of steps are {} {}'.format(type(steps), steps)
        self.steps = steps

    def price_option(self, option, round_digit=4):

        self.strike = option.strike

        # Calculate delta_t, u, d, a and p
        delta_t = option.expiry * 1.0 / self.steps
        u = exp(option.vol * sqrt(delta_t))
        d = 1 / u
        self.a = exp(option.rate * delta_t)
        self.p = (self.a - d) / (u - d)
        # print 'u is {}, d is {}, a is {}, p is {}'.format(u, d, self.a, self.p)

        # Construct a tree
        self.tree = []  # TODO: replace list with custom tree container which can print it's content
        for lv in range(self.steps + 1):
            # The root is level 0; at level i there are i + 1 nodes
            # Calculate spot price for nodes from root to bottom
            if lv == 0:
                nodes_at_lv = [TreeNode(option.spot)]
            else:
                nodes_at_lv = []  # the list of nodes at level lv
                for idx in range(lv + 1):
                    if idx == 0:
                        node = TreeNode(self.tree[lv - 1][idx].spot * u)
                    else:
                        node = TreeNode(self.tree[lv - 1][idx - 1].spot * d)
                    nodes_at_lv.append(node)

            self.tree.append(nodes_at_lv)

        self.tree.reverse()  # Reverse the tree as we calculate values from bottom to root
        for i, tree_at_lv in enumerate(self.tree):
            for j, node in enumerate(tree_at_lv):
                if i == 0:  # bottom level, no next level
                    node.opt = self.get_opt_4_last_step(node.spot, option.type)
                else:  # not bottom level, calculate option price from next level
                    node.opt = self.get_opt_4_prev_step(self.tree[i - 1][j].opt, self.tree[i - 1][j + 1].opt)

                    # print 'spot price =', node.spot, 'option price =', node.opt

        return round(self.tree[i][j].opt, round_digit)

    def get_opt_4_last_step(self, spot, otype):
        """Get option price for the last step:
        Input the spot price for the last step and return its option price
        """
        if otype == OptionType.PUT:
            if spot >= self.strike:
                return 0
            else:
                return self.strike - spot
        elif otype == OptionType.CALL:
            if spot <= self.strike:
                return 0
            else:
                return spot - self.strike

    def get_opt_4_prev_step(self, up_opt, down_opt):
        """Get option price for the previous step:
        Input 2 option prices at step N and return the option price at step N - 1
        """
        return (self.p * up_opt + (1 - self.p) * down_opt) / self.a


class TreeNode(object):
    def __init__(self, spot):
        self.spot = spot
        self.opt = None
