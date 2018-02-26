"""Model initialization script."""
from models import HeuristicalModel
from heuristics import (
        MovingAverageHeuristic)

if __name__ == '__main__':
    import argparse
    
    import numpy as np

    parser = argparse.ArgumentParser()
    parser.add_argument(
            'groups',
            choices=[1,],
            type=int,
            help='heuristic groups used in the simulation')
    parser.add_argument(
            'weights',
            type=lambda s: [float(weight) for weight in s.split(',')],
            help='weights for each excess demand function')
    parser.add_argument(
            'init_price',
            type=float,
            help='initial price of the stock')
    parser.add_argument(
            'rand_steps',
            type=int,
            help='number of steps to perform during the initial random walk')
    parser.add_argument(
            'steps',
            type=int,
            help='number of steps to perform after the random walk')
    parser.add_argument(
            'sigma',
            type=float,
            help='scaler multiple of random values during the initial walk')
    parser.add_argument(
            'num_trials',
            type=int,
            help='number of simulations to perform')
    parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='increase output verbosity')
    
    args = parser.parse_args()
    
    # Define the heuristic groups to be passed to the model
    if args.groups == 1:
        heuristics = [MovingAverageHeuristic(m=1, n=5)]
    if len(args.weights) != len(heuristics):
        raise Exception('Mismatch between the number of weights'
                        ' and the number heuristics.')

    model = HeuristicalModel(
            heuristics,
            args.weights,
            args.rand_steps,
            args.init_price,
            args.sigma)

    results = np.zeros((args.num_trials, args.rand_steps + args.steps),
                       dtype=np.float32)
    
    for i in range(args.num_trials):
        results[i] = model.simulate(args.steps)

    if args.verbose:
        import matplotlib.pyplot as plt
        
        title = '$g=%d$ ' % args.groups
        title += ",".join(['$a_{%d}=%.1f$ ' % (i, weight) \
                          for i, weight in enumerate(args.weights)])
        title += '$w=%.2f$ $r=%d$ $s=%d$ $p_{0}=%.2f$ $\sigma=%.2f$' \
                 % (0.01, args.rand_steps, args.steps, args.init_price, 
                    args.sigma)

        # Appraently if the number of subplots is 1,
        # calling plt.subplots does not return an array 
        # of axis, so array indexing throws an exception...
        if args.num_trials == 1:
            plt.plot(results[0])
            plt.axvline(args.rand_steps, color='red')
        else:
            f, axis = plt.subplots(args.num_trials, sharex=True)
            f.subplots_adjust(hspace=0.5)
            for i in range(args.num_trials):
                axis[i].plot(results[i])
                axis[i].axvline(args.rand_steps, color='red')
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        
        plt.suptitle(title) 
        plt.show()
