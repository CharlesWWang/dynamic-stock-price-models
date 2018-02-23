'''
Implementation of fuzzy set membership functions.

Reference
https://arxiv.org/ftp/arxiv/papers/1401/1401.1888.pdf

'''
import numpy as np

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