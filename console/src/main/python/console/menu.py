# -*- coding: utf-8 -*-
"""
Created on Sat May 23 13:02:04 2015

@author: Niel
"""

class MenuItems():
    
    @staticmethod
    def info(message):
        print message        
        
    @staticmethod
    def blankline():
        print ''
    
    @staticmethod       
    def dash(mult):
        print '-'*mult
    
    @staticmethod
    def hashes(mult):
        print '#'*mult
    
    @staticmethod
    def space(mult):
        print' '*mult
    
    @staticmethod
    def error(message):
        print 'ERROR: ' + message
        
        
    @staticmethod
    def options(dict_options):
        keys = dict_options.keys()
        keys.sort()
        for key in keys:
            print key + '.' + ' ' + dict_options[key]
        
        
class MenuBuilder():
    
    
    def __init__():
        '''
        '''
        
        
    def add(self):
        '''
        '''
        
    def show(self):
        '''
        '''