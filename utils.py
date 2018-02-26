"""Utilities and functions used by various heuristics"""
import numpy as np

def moving_average(signal, t, n):
    """
    Return the moving average of `signal` at time `t`.

    Averaging is done over the most recent `n` observations.
    """
    return np.mean(signal[t-n+1:t+1])

def percent_change(a, b):
    """Return the approximate percent change from `b` to `a`.

    Note that log-ratio approximate percent changes well
    when the ratio of final price to initial price is close to 1.
    """
    return np.log(a) - np.log(b)
