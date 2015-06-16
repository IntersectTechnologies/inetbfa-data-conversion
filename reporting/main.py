import get_data as gd
import numpy as np
import pandas as pd
import os.path

## Manual input ##

date = '2014-03-28'

##
base_dirs = {
    'root': 'C:/Users/nielswart/repos/riskanalysis',
    'data': 'C:/Users/nielswart/repos/riskanalysis/data'
}

# Get client list and data
clients = gd.get_clients(os.path.join(base_dirs['root'], 'clients', 'clients.xlsx'), 'clients')

# create report directories for new data if not already exists

# Get Price Data  
sheetname = '1. Comparison'
filename = '2014-04-07.xlsx'
price_path = os.path.join(base_dirs['data'], filename)
pricedata = gd.get_pricedata_xl(price_path, sheetname)

# Get Datamap
dmap = gd.get_datamap_csv(os.path.join(base_dirs['data'], 'datamap.csv'))

# common currency

# log returns

# proxy data
    
## FOR EACH client DO
for client in clients.client_code:

    client_dirs = {
        'root' : os.path.join(base_dirs['root'], 'clients', client['code']),
        'report' : os.path.join(base_dirs['root'], 'clients', client['code'], 'reports'),
        'metrics' : os.path.join(base_dirs['root'], 'clients', client['code'], 'metrics'),
        'data': os.path.join(base_dirs['root'], 'clients', client['code'], 'data')
    }
    
    report = os.path.join(client_dirs['report'], date)
    
    # Get Exposure data
    exp = gd.get_exposure_data(os.path.join(report, 'exposure.xlsx'), 'exposure')
    
    # Get Portfolio Data  
    portf = 
    
    # calculate portfolio returns
    
    # Calculate Risk Metrics
    
    
    # Generate Excel Report
    filename = client + ' Portfolio Risk Report ' + date + '.xlsx'

## EMAIL REPORTS
