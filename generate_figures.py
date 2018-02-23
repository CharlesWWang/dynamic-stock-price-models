import numpy as np
import matplotlib.pyplot as plt

from fuzzy import *

def generate_fig_1_2():
    # Generate Fig. 1 and Fig. 2 from the paper.
    #
    # Not yet sure how to adjust text size automatically
    # based on the figure size. Values below are hand tuned
    # to work with a maximized figure.
    w = 0.01

    price_change_membership_functions = [
            ShelfMembershipFn(-2*w, -3*w),
            SymmetricMembershipFn(-3*w, -w),
            SymmetricMembershipFn(-2*w, 0),
            SymmetricMembershipFn(-w, w),
            SymmetricMembershipFn(0, 2*w),
            SymmetricMembershipFn(w, 3*w),
            ShelfMembershipFn(2*w, 3*w)]


    action_membership_functions = [
            ShelfMembershipFn(-0.2, -0.4),
            SkewdMembershipFn(-0.4, -0.2, -0.1),
            SymmetricMembershipFn(-0.2, 0),
            SymmetricMembershipFn(-0.1, 0.1),
            SymmetricMembershipFn(0, 0.2),
            SkewdMembershipFn(0.1, 0.2, 0.4),
            ShelfMembershipFn(0.2, 0.4)]

    price_change_bank = MembershipBank(price_change_membership_functions)
    action_bank = MembershipBank(action_membership_functions)

    linspace = np.linspace(-4*w, 4*w, 10000)
    f, axarr = plt.subplots(2, 1, figsize=(16, 10)) 

    axarr[1].set_xlim([-0.4, 0.4])
    axarr[0].set_title('Fuzzy sets quantifying price percentage change')
    axarr[0].set_xlabel('x')
    axarr[0].set_ylabel('$\mu$')
    axarr[1].set_title('Fuzzy sets quantifying buy (sell) signals')
    axarr[1].set_xlabel('ed')
    axarr[1].set_ylabel('$\mu$')

    fontdict={'size': 12, 'weight': 'normal'}

    for i, j in zip(range(-3, 4), ['NL', 'NM', 'NS', 'AZ', 'PS', 'PM', 'PL']):
        axarr[0].text(i*w, 0.5, j, fontdict=fontdict)

    for i, j in zip([-0.35, -0.2, -0.1, 0., 0.1, 0.2, 0.35], ['SB', 'SM', 'SS', 'N', 'BS', 'BM', 'BB']):
        axarr[1].text(i, 0.5, j, fontdict=fontdict) 

    # f.subplots_adjust(hspace=0.1)

    for i in range(7):
        axarr[0].plot(linspace, [price_change_membership_functions[i].grade(signal) for signal in linspace])
        axarr[1].plot(linspace*10, [action_membership_functions[i].grade(signal) for signal in linspace*10])

    f.tight_layout()
    plt.show()

if __name__ == '__main__':
    generate_fig_1_2()