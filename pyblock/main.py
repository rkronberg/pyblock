import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from block_average import Blocked


def parse():

    # Parse command line arguments

    p = ArgumentParser(description='Error estimation by block averages')
    p.add_argument('-i', '--input', required=True, help='Input file')
    p.add_argument('-n', '--bmin', default=10, type=int,
                   help='Smallest number of blocks')
    p.add_argument('-p', '--plot', action='store_true',
                   help='Plot statistical inefficiency fit')

    return vars(p.parse_args())


def main():

    args = parse()
    inp = args['input']
    bmin = args['bmin']
    isplot = args['plot']

    print('Computing average with error estimate for \
        correlated timeseries %s' % inp)

    # Load data
    data = np.loadtxt(inp)

    # Proceed with the block averaging
    blk = Blocked(data, bmin)
    blk.run()

    # Compute an error estimate for the average
    blk.error()

    print('\n<x> = %.4f +/- %.4f' % (blk.run_ave, blk.err))

    # Visual evaluation
    if(isplot):
        plt.plot(blk.sizes, blk.s)
        plt.plot(blk.sizes, blk.fit(blk.sizes, *blk.popt))
        plt.axhline(blk.popt[0])
        plt.show()


if __name__ == '__main__':
    main()
