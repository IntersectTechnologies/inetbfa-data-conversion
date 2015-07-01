import numpy as np
import pandas as pd

def get_exposure_data(path, sheetname):
    '''
    Read portfolio exposure from xlsx file with the following important columns:
    
    stype - security type   C \n
    sname                   E \n
    counterpart             G \n
    currency_code           I \n
    nav_pct                 L \n
    exposure                M \n
    exposure_pct            N \n
    country_code            Q \n
    isin                    U \n
    ticker                  Y \n
    exchange_code           AA \n
    sector_code             AB \n
    number_of_shares        AD \n
    market_price            AE \n
    '''
    
    cols = 'C,E,G,I,L,M,N,Q,U,Y,AA,AB,AD,AE'
    
    exposure = pd.read_excel(path, sheetname, header = 0, parse_cols = cols)    
    return exposure

def get_pricedata_xl(path, sheetname):
    '''
    '''
    pricedata = pd.read_excel(path, sheetname, header = 0, index_col = 0)

    return pricedata

def get_pricedata_csv(path):
    '''
    '''
    pricedata = pd.read_csv(path, index_col = 0)

    return pricedata

def get_portfoliodata(path, sheet):
    '''
    '''

    portf = pd.read_excel(path, sheet, header = 0, index_col = 0)
    return portf


def get_datamap_xl(path, sheetname):
    '''
    '''



def get_datamap_csv(path):
    '''
    '''

    mapdata = pd.read_csv(path, sep = ',', index_col = 0)

    return mapdata
    
def get_clients(path, sheetname):
    '''
    Get list of clients and their data
    '''
    
    clients = pd.read_excel(path, sheetname)
    
    return clients