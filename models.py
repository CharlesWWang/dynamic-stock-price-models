"""Stock price fluctuation models"""
import numpy as np


class HeuristicalModel(object):
    """Implementation of the price dynamical model based on heuristics"""
    def __init__(
            self,
            heuristics,
            weights,
            rand_steps,
            init_price,
            sigma):
        
        self.heuristics = heuristics
        self.weights = weights
        self.rand_steps = rand_steps
        self.init_price = init_price
        self.sigma = sigma
    
    def simulate(self, steps):
        """Simulate `steps` iterations of the model.

        First, a random walk of `self.rand_steps` is performed
        to generate an initial set of price points.
        """
        signal = np.zeros(self.rand_steps + steps)
        signal[0] = self.init_price
        signal[1:self.rand_steps] = np.exp(self.sigma * \
                np.random.normal(size=(self.rand_steps-1)))
        signal[:self.rand_steps] = np.cumprod(signal[:self.rand_steps])
        
        excess_demands = np.zeros_like(self.heuristics)
        for step in range(self.rand_steps, self.rand_steps+steps):
            for i, heuristic in enumerate(self.heuristics):
                excess_demands[i] = heuristic.excess_demand(
                        signal, step-1)

            avg_excess_demand = np.dot(excess_demands, self.weights)
            signal[step] = signal[step-1] * np.exp(avg_excess_demand)

        return signal

