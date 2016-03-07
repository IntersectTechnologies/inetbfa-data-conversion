from os import path, listdir, makedirs
import re, codecs
import datetime as dt
import calendar as cal
import pandas as pd
import string

from datamanager.envs import *
from datamanager.load import *
from datamanager.adjust import calc_adj_close, calc_booktomarket
from datamanager.utils import last_month_end

fields = marketdata_fields()

# paths
mergein_old = MASTER_DATA_PATH
mergein_new = CONVERT_PATH

closepath = path.join(MERGED_PATH, "Close.csv")
divpath = path.join(MERGED_PATH, "Dividend Ex Date.csv")
bookvaluepath = path.join(MERGED_PATH, "Book Value per Share.csv")

def get_all_equities():
    new_all, _, _, _ = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return new_all

def get_current_listed():
    new_all, current, newly_listed, delisted = get_all_equities_from_data(MERGED_PATH, CONVERT_PATH, 'Close')
    return current_set

def convert_data(dependencies, targets):
    '''
    '''
    dependencies = list(dependencies)
    new_data = load_intebfa_ts_data(dependencies[0])
    new_data = new_data.dropna(how='all')
    new_data.to_csv(targets[0])

def create_report():
    '''
    '''
    reportdata = {}
    columns = ['startdate', 'enddate', 'number', 'comments']
    with open('report.html', 'a') as report_html:
        report_html.write('<html>Report')
        report_html.write('<head>')
        report_html.write('</head>')
        report_html.write('<body>')
        report_html.write('<h1>Conversion Report</h1>')
        for f in listdir(CONVERT_PATH):
            file = f
           
            report_html.write('<h3>' + f + '</h3>')
            data = load_ts(path.join(CONVERT_PATH, f))
            reportdata['startdate'] = [data[ticker].first_valid_index() for ticker in data.columns]
            reportdata['enddate'] = [data[ticker].last_valid_index() for ticker in data.columns]
            reportdata['number'] = [data[ticker].count() for ticker in data.columns]

            report = pd.DataFrame(reportdata, index = data.columns, columns = columns)
            report_html.write('<div>' + report.to_html() + '</div>')
        
        report_html.write('<h1>Merge Report</h1>')
        for f in listdir(MERGED_PATH):
            file = f
           
            report_html.write('<h3>' + f + '</h3>')
            data = load_ts(path.join(MERGED_PATH, f))
            
            reportdata['startdate'] = [data[ticker].first_valid_index() for ticker in data.columns]
            reportdata['enddate'] = [data[ticker].last_valid_index() for ticker in data.columns]
            reportdata['number'] = [data[ticker].count() for ticker in data.columns]

            report = pd.DataFrame(reportdata, index = data.columns, columns = columns)
            report_html.write('<div>' + report.to_html() + '</div>')

        report_html.write('</body>')
        report_html.write('</html>')

def merge_data(task): 
  
    new = load_ts(path.join(CONVERT_PATH, task.name.split(':')[1] + '.csv'))
    old = load_ts(path.join(MASTER_DATA_PATH, task.name.split(':')[1] + '.csv'))
    
    merged = empty_dataframe(get_all_equities())
    merged.update(old)
    merged.update(new)

    merged = merged.dropna(how='all')
    merged.to_csv(task.targets[0])

def calc_adjusted_close(dependencies, targets):
    all_equities = get_all_equities()
    adj_close = calc_adj_close(closepath, divpath, all_equities)
    adj_close.to_csv(targets[0])

def booktomarket(dependencies, targets):
    b2m = calc_booktomarket(closepath, bookvaluepath)
    b2m.to_csv(targets[0])

def swapaxes(dependencies, targets):
    
    temp = {}
    for d in dependencies:
        field = d.split("\\")[-1].split(".")[0]
        temp[field] = pd.read_csv(d, sep = ',', index_col = 0, parse_dates=True)

    # now create panel
    panel = pd.Panel(temp)
    out = panel.swapaxes(0, 2)

    for ticker in out.items:
        out[ticker].dropna(how='all').to_csv(path.join(CONVERT_PATH, "tickers", ticker + '.csv'), index_label = "Date")

##########################################################################################
# DOIT tasks
##########################################################################################

# 1
def task_convert():
    for f in fields:
        yield {
            'name':f,
            'actions':[convert_data],
            'targets':[path.join(CONVERT_PATH, f+ '.csv')],
            'file_dep':[path.join(DL_PATH, f + '.xlsx')],
        }

# 2
def task_merge():
    for f in fields:
        yield {
            'name':f,
            'actions':[merge_data],
            'targets':[path.join(MERGED_PATH, f + '.csv')],
            'file_dep':[path.join(mergein_new, f + '.csv'), path.join(mergein_old, f + '.csv')]
        }
# 3
def task_adjusted_close():
    return {
        'actions':[calc_adjusted_close],
        'file_dep': [closepath,
                     divpath],
        'targets':[path.join(MERGED_PATH, "Adjusted Close.csv")]
    }

# 5
def task_book2market():
    return {
        'actions':[booktomarket],
        'file_dep': [closepath,
                     bookvaluepath],
        'targets':[path.join(MERGED_PATH, "Book-to-Market.csv")]
    }

# 6
def task_data_per_ticker():
    files = [path.join(CONVERT_PATH, f + '.csv') for f in fields]
    return {
        'actions':[swapaxes],
        'file_dep': files,
        'targets':[path.join(CONVERT_PATH, "tickers")]
    }

def task_report():
    return {
        'actions':[create_report],
        'task_dep':['merge']
    }