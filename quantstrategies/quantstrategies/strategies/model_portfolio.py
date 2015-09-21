import pandas as pd

def calc_means(data, fields, period = '1M'):
    means = {}
    for f in fields:
        data[f].fillna(method = 'pad', inplace=True)
        means[f] = data[f].last(period).mean()
        
        if type(means[f]) != pd.Series:
            raise TypeError
        
    return means     

class ModelPortfolio(object):
    '''
    '''
    
    def __init__(self, start_date, end_date):
        '''
        '''
        self.start_date = start_date
        self.end_date = end_date
        
    def save(self, fpath):
        self.run().to_excel(fpath)