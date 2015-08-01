# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:22:03 2015

@author: Niel Swart
"""

import pandas as pd

class Node:
    def __init__(self, data):
        '''
        '''
        self.data = data

    def _action_(self, **kwargs):
        '''
        Call a node with a named functions to apply to the data
        It will return a DataFrame object with the keys as index
        '''
        tmp = {}
        for k, func in kwargs.items():
            tmp[k] = func(self.data)
        
        return Node(pd.DataFrame.from_dict(tmp, orient='index'))

    def transform(self, func):
        tmp = func(self.data)
        return Node(tmp)

    def stats(self, **kwargs):
        return self._action_(**kwargs)

    def filter(self, *args):
        filtered = self.data.columns

        for filter in args:
            filtered = filtered.intersection(filter)

        return Node(self.data[filtered])
        

