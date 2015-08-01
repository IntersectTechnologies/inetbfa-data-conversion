from os import path, listdir
import re, codecs
import logging

import datamanager.tasks as tasks
from console.menu import MenuItems

# logging
logging.basicConfig(filename='datamanager.log', level=logging.INFO)


def main():
    intro()
    main_menu()
    
def intro():
    MenuItems.info('##########################################')
    MenuItems.info('# Financial Data Management Application  #')
    MenuItems.info('#                                        #')
    MenuItems.info('#   ------- Version 1.0.1  ----------    #')
    MenuItems.info('#                                        #')
    MenuItems.info('#              2015/07/01                #')
    MenuItems.info('#                                        #')
    MenuItems.info('#           Copyright (c) 2015           #')
    MenuItems.info('#      Intersect Technologies CC         #')
    MenuItems.info('#                                        #')
    MenuItems.info('##########################################')

def main_menu():
    
    options = {
        '1': 'Update Reference Data',
        '2': 'Update Market Data',
        '3': 'Calculate Adjusted Close',
        '4': 'Sync data with slaves' ,
        '5': 'Generate NWU Momentum Portfolio'
    }    
    
    MenuItems.blankline()
    MenuItems.info('Choose an option:')
    MenuItems.dash(50)
    MenuItems.options(options)
    MenuItems.dash(50)
    MenuItems.info('X to quit program')
    MenuItems.blankline()
    inp = raw_input('Enter option and press ENTER: ')

    if inp.upper()=='X':
        # Exit
        return
    else:
        if int(inp) >= 1 and int(inp) <= len(options):
            logging.info('Input: ' + inp + ' ' + options[inp])
            sub_menu(int(inp)) 
        else:
            logging.warning('Invalid choice in Main Menu: ' + inp)

def sub_menu(choice):
    '''
    '''
    
    def call(menu_choice):
        menu = smenu[menu_choice][0]
        func = smenu[menu_choice][1]
        
        menu()
        func()
        main_menu()
    
    def ref_data():
        MenuItems.blankline()
        MenuItems.dash(50)
        MenuItems.blankline()
        MenuItems.info('1. Updating JSE Reference Data...')
        MenuItems.blankline()
        MenuItems.dash(50)
        MenuItems.blankline()
    
    def market_data():
        MenuItems.blankline()
        MenuItems.dash(50)
        MenuItems.blankline()
        MenuItems.info('2. Updating JSE Market and Dividend Data...')
        MenuItems.blankline()
        MenuItems.dash(50)
    
    def calc_adj_close():
        MenuItems.blankline()
        MenuItems.dash(50)
        MenuItems.blankline()
        MenuItems.info('3. Calculating Adjusted Close Data...')
        MenuItems.blankline()
        MenuItems.dash(50)
        
    def sync_data_menu():
        MenuItems.info('4. Syncing data from Master to all Registered Slaves')
        
    def nwu_mom_menu():
        MenuItems.info('5. Generating NWU Momentum Portfolio')
        
    smenu = {
        1: (ref_data, tasks.task_update_ref_data),
        2: (market_data, tasks.task_update_market_data),
        3: (calc_adj_close, tasks.task_calc_adjusted_close),
        4: (sync_data_menu, tasks.task_sync_data),
        5: (nwu_mom_menu , tasks.task_update_nwu_momentum_portfolio)
    }
    
    call(choice)

if __name__ == "__main__":
    main()