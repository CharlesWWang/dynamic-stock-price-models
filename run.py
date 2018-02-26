"""Model initialization script."""
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
            'num_trials',
            type=int,
            help='number of simulations to perform')
    parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='increase output verbosity')
    
    args = parser.parse_args()
