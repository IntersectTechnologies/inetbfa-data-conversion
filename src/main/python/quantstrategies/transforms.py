"""
Copyright 2015 Intersect Technologies CC

@author: Niel Swart
@date: 2015/06/25

"""

def momentum(window):
    """
    """

    mom = np.log(window.end) - np.log(window.start)
