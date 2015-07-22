"""
Copyright 2015 Intersect Technologies CC

@author: Niel Swart
@date: 2015/06/25

"""

def momentum(window):
    '''
    '''

    mom = np.log(window.end) - np.log(window.start)

def last_mean(data, period = '1M'):
    '''
    '''

    data.fillna(method = 'pad', inplace=True)
    means = data.last(period).mean()
        
    if type(means) != pd.Series:
            raise TypeError
        
    return means