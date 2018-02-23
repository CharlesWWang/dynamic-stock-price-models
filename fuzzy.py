'''
Implementation of fuzzy set membership functions.

Reference
https://arxiv.org/ftp/arxiv/papers/1401/1401.1888.pdf

'''
from abc import abstractmethod

class FuzzyMembershipFn(object):
    """
    Abstract class representing fuzzy set membership functions.

    Specific membership functions are implemented by child classes.
    """
    @abstractmethod
    def grade(self, item):
        pass

class SymmetricMembershipFn(FuzzyMembershipFn):
    """Symmetric piece-wise linear membership function."""
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.center = (start + stop) / 2

    def grade(self, item):
        if item >= self.start and item <= self.stop:
            return 1 - np.abs(item - self.center) / (self.center - self.start)
        else:
            return 0

class SkewdMembershipFn(FuzzyMembershipFn):
    """Skewed piece-wise linear membership function."""
    def __init__(self, start, center, stop):
        self.start = start
        self.center = center
        self.stop = stop
    
    def grade(self, item):
        if item >= self.start and item <= self.center:
            return (item - self.start) / (self.center - self.start)
        elif item >= self.center and item <= self.stop:
            return (self.stop - item) / (self.stop - self.center)
        else:
            return 0
            
class ShelfMembershipFn(FuzzyMembershipFn):
    """Piece-wise linear shelf membership function."""
    def __init__(self, start, center):
        self.start = start
        self.center = center

        if self.center > self.start:
            self.comp = np.greater
        elif self.center < self.start:
            self.comp = np.less
        else:
            raise ValueError("Improper shelf parameters.")

    def grade(self, item):
        if self.comp(item, self.center):
            return 1
        elif (not self.comp(item, self.start)) and item != self.start:
            return 0
        else:            
            return (item - self.start) / (self.center - self.start)

class MembershipBank(object):
    """A collection of membership functions that grade any input signal."""
    def __init__(self, membership_functions):
        self.membership_functions = membership_functions

    def grade(self, signal):
        """
        Return membership grades of the signal.

        The signal is graded by each membership function in the bank.
        """
        return np.array([membership_function.grade(signal) \
                for membership_function in self.membership_functions]) 
    
    @property
    def centers(self):
        """
        Return earliest (in abs. value) signals that are full members.
        
        Returned value is a vector containing the center of each
        membership function in the bank.
        """
        return np.array([membership_function.center \
                for membership_function in self.membership_functions])

    def __getitem__(self, key):
        """Slicing a MembershipBank returns a new MembershipBank."""
        return MembershipBank(self.membership_functions[key])


if __name__ == '__main__':
    # Generate Fig. 1 and Fig. 2 from the paper.
    #
    # Not yet sure how to adjust text size automatically
    # based on the figure size. Values below are hand tuned
    # to work with a maximized figure.
    import numpy as np
    import matplotlib.pyplot as plt
    
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

    w = max(w, 0.01)
    linspace = np.linspace(-4*w, 4*w, 10000)
    f, axarr = plt.subplots(2, 1, figsize=(8, 5)) 
    
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
    
    f.subplots_adjust(hspace=0.5)

    for i in range(7):
        axarr[0].plot(linspace, [price_change_membership_functions[i].grade(signal) for signal in linspace])
        axarr[1].plot(linspace*10, [action_membership_functions[i].grade(signal) for signal in linspace*10])

    plt.show()
    
    
