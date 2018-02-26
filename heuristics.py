"""Implementations of heuristics describing investor strategies."""
import numpy as np

from abc import abstractmethod
from utils import (
        moving_average, percent_change)
from fuzzy import (
        SymmetricMembershipFn,
        SkewdMembershipFn,
        ShelfMembershipFn,
        MembershipBank)


# Fuzzy membership sets used in heuristics
INVESTOR_SIGNALS = {
    'SellBig': ShelfMembershipFn(-0.2, -0.4),
    'SellMedium': SkewdMembershipFn(-0.4, -0.2, -0.1),
    'SellSmall': SymmetricMembershipFn(-0.2, 0),
    'Neutral': SymmetricMembershipFn(-0.1, 0.1),
    'BuySmall': SymmetricMembershipFn(0, 0.2),
    'BuyMedium': SkewdMembershipFn(0.1, 0.2, 0.4),
    'BuyBig': ShelfMembershipFn(0.2, 0.4)
}

w = 0.01  # TODO: Figure out a good way to pass this as a cmd argument.
PRICE_PERCENT_CHANGE_SIGNALS = {
    'NegativeLarge': ShelfMembershipFn(-2*w, -3*w),
    'NegativeMedium': SymmetricMembershipFn(-3*w, -w),
    'NegativeSmall': SymmetricMembershipFn(-2*w, 0),
    'AroundZero': SymmetricMembershipFn(-w, w),
    'PositiveSmall': SymmetricMembershipFn(0, 2*w),
    'PositiveMedium': SymmetricMembershipFn(w, 3*w),
    'PositiveLarge': ShelfMembershipFn(2*w, 3*w)
}

class Heuristic(object):
    """Abstract representation of an investment strategy."""
    @abstractmethod
    def excess_demand(self):
        pass


class MovingAverageHeuristic(Heuristic):
    """
    Heuristic 1: A buy (sell) signal is generated if a shorter
    moving average of the price is crossing a longer moving
    average of the price from below (above). Usually, the larger the
    difference between the two moving averages, the stronger the
    buy (sell) signal. But, if the difference between the two moving
    averages is too large, the stock may be over-bought (over-sold),
    so a small sell (buy) order should be placed to safeguard the
    investment.
    """
    def __init__(self, m, n):
        self.m = m
        self.n = n

        self.ppc_signals = MembershipBank([
                PRICE_PERCENT_CHANGE_SIGNALS[amount] for amount in \
                        ['PositiveSmall', 'PositiveMedium', 'PositiveLarge',
                         'NegativeSmall', 'NegativeMedium', 'NegativeLarge',
                         'AroundZero']])
        self.investor_signals = MembershipBank([
                INVESTOR_SIGNALS[action] for action in \
                        ['BuySmall', 'BuyBig', 'SellMedium', 'SellSmall',
                         'SellBig', 'BuyMedium', 'Neutral']])

    def excess_demand(self, signal, time):
        """Excess demand function for moving averages based heuristic (group 1).""" 
        m_window_average = moving_average(signal, time, self.m)
        n_window_average = moving_average(signal, time, self.n)
        price_change = percent_change(m_window_average, n_window_average)

        price_change_strengths = self.ppc_signals.grade(price_change)
        investor_signal_strengths = self.investor_signals.centers

        result = np.dot(investor_signal_strengths, price_change_strengths)
        result /= np.sum(price_change_strengths)

        return result


 
 
