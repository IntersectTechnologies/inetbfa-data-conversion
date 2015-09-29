
import pandas as pd

def calc_means(data, period = '1M'):
    
    means = {}
    for f in iter(data):
        data[f].fillna(method = 'pad', inplace=True)
        means[f] = data[f].last(period).mean()
        
        if type(means[f]) != pd.Series:
            raise TypeError
        
    return means