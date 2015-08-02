# -*- coding: utf-8 -*-
"""
Created on Sat May 23 15:22:03 2015

@author: Niel Swart
"""

import pandas as pd
from functools import partial
from uuid import uuid4

# TODO: create callback class / partial function that wraps the repetive logic of callbacks and node registration
class Node(object):
    def __init__(self, data=None, name = 'Node'):
        '''
        '''

        self.name = name
        self.guid = uuid4()
        self.data = data
        self.callbacks = []
        self.from_nodes = []

    def __call__(self):
        '''
        '''

        print 'Node ' + str(self.guid) + ' called...'

        # wait until all from nodes have been called...
        if len(self.callbacks) > 0:
            for cb in self.callbacks:
                cb()
        else:
            print('No callbacks registered...')

    def to_(self, node):
        '''
        '''

        def copy():
            node.data = self.data.copy()
            node()

        self.callbacks.append(copy)
        return self

    def from_(self, *nodes):
        '''
        '''
        
        self.append(nodes);

        
class SourceNode(Node):
    '''
    '''

    def __init__(self, data=None, name = 'SourceNode'):
        '''
        '''

        super(SourceNode, self).__init__(data, name = 'SourceNode')

    def transform(self, func):
        
        node = SourceNode()
        def transformfunc():
            print('Calling transform on ' + str(self.guid))
            tmp = func(self.data)
            node.data = tmp
            node()

        self.callbacks.append(transformfunc)
        return node

    def stats(self, **kwargs):
        '''
        Call a node with a named functions to apply to the data
        It will return a DataFrame object with the keys as index
        '''

        node = SourceNode()
        def statsfunc():
            print('Calling stats on ' + str(self.guid))
            tmp = {}
            for k, func in kwargs.items():
                tmp[k] = func(self.data)
        
            node.data = pd.DataFrame.from_dict(tmp, orient='index')
            node()

        self.callbacks.append(statsfunc)
        return node

    def filter(self, *args):

        node = SourceNode()
        node.from_nodes.append(self)
        def filterfunc():
            print('Calling filter on ' + str(self.guid))
            filtered = self.data.columns

            for filter in args:
                filtered = filtered.intersection(filter)

            node.data = self.data[filtered].copy()
            node()

        self.callbacks.append(filterfunc)
        return node

class StrategyNode(Node):
    '''
    '''

    def __init__(self, data=None, name = 'StrategyNode'):
        '''
        '''

        super(StrategyNode, self).__init__(data, name = 'StrategyNode')

class SinkNode(Node):
    '''
    '''

    def __init__(self, data=None, name = 'SinkNode'):
        '''
        '''

        super(SinkNode, self).__init__(data, name = 'SinkNode')

    def report(self):

        def printer():
            print(self.data)

        self.callbacks.append(printer)