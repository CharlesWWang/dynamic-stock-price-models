"""Model initialization script."""
from models import HeuristicalModel
from heuristics import *

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
            'heuristics',
            nargs='+',
            help='heuristics used in the simulation')
    parser.add_argument(
            'weights',
            nargs='+',
            type=float,
            help='weights for each excess demand function')
    parser.add_argument(
            'w', 
            type=float,
            help='numerical definition of a small price change')
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
            'num_trials',
            type=int,
            help='number of simulations to perform')
    parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='increase output verbosity')
    
    args = parser.parse_args()
    
    heuristics = [eval(heuristic) for heuristic in args.heuristics]
    model = HeuristicalModel(
            heuristics,
            args.weights,
            args.w)

    model.generate_init_data(args.rand_steps, args.init_price)    
    results = np.zeros((args.num_trials, args.rand_steps + args.steps),
                       dtype=np.float32)
    
    for i in range(args.num_trials):
        results[i] = model.simulate(args.steps)

    if args.verbose:
        f, axis = plt.subplots(args.num_trials, sharex=True)
        f.subplots_adjust(hspace=0.5)
        for i in range(args.num_trials):
            axis[i].plot(results[i])
            axis[i].axvline(args.rand_steps, color='red')
        plt.show()
