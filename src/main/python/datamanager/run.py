from os import path, listdir
import re, codecs
import logging

from envs import *
from datamodel import MarketData, Dividends, get_equities, set_equities, update_listing_status
from process_downloads import MarketDataProcessor, ReferenceProcessor
from sync import create_dir, sync_latest_master, sync_master_slave
from console.menu import MenuItems
from adjust import calc_adj_close

# logging
logging.basicConfig(filename='datamanager.log', level=logging.INFO)


def local_file(filename):
    return codecs.open(
        path.join(path.dirname(__file__), filename), 'r', 'utf-8'
    )
    
version = re.search(
    "^__version__ = \((\d+), (\d+), (\d+)\)",
    local_file('__init__.py').read(),
    re.MULTILINE
).groups()


fields = MarketData.fields
fields.extend(Dividends.fields)
    
def main():
    intro()
    main_menu()
    
def intro():
    MenuItems.info('##########################################')
    MenuItems.info('# Financial Data Management Application  #')
    MenuItems.info('#                                        #')
    MenuItems.info('#   ------- Version ' + '.'.join(version) + ' ----------    #')
    MenuItems.info('#                                        #')
    MenuItems.info('#              2015/04/15                #')
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
        1: (ref_data, update_ref_data),
        2: (market_data, update_market_data),
        3: (calc_adj_close, calc_ac),
        4: (sync_data_menu, sync_data),
        5: (nwu_mom_menu , nwu_momentum)
    }
    
    call(choice)

def calc_ac():
    adj_close = calc_adj_close()
    adj_close.to_csv(path.join(MASTER_DATA_PATH, 'jse' , 'equities', 'daily', 'Adjusted Close.csv'))

def nwu_momentum():
    import quantstrategies.nwu_momentum
        
def update_ref_data():
    '''
    '''
    ref = get_equities()
    refp = ReferenceProcessor()
    refnew = refp.load_new(DL_PATH)
    
    set_equities(refp.update(ref, refnew))
    update_listing_status()    

def update_market_data():
    '''
    '''
    
    avail_fields = [f.split('.')[0] for f in listdir(DL_PATH)]
    ref = get_equities()
    prc = MarketDataProcessor(ref)
    create_dir(path.join(MASTER_DATA_PATH, 'latest_updates'))
    
    logging.info('Start processing updated data files...')
    for f in avail_fields:
        if f in fields and f != 'Reference':
            logging.info('Processing ' + f)
            merged = prc.load_and_merge(f, MarketData.filepath, DL_PATH)
            logging.info('Saving data to: '+ path.join(MASTER_DATA_PATH, 'latest_updates', f + '.csv'))
            prc.save(merged, path.join(MASTER_DATA_PATH, 'latest_updates', f + '.csv'))
            logging.info('Finished processing file...')
    
    logging.info('Finished processing Market and Dividend Data')

def sync_data():
    '''
    '''
    
    sync_latest_master()
    sync_master_slave()
    
if __name__ == "__main__":
    main()