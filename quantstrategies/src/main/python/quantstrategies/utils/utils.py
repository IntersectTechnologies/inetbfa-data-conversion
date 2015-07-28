import datetime as dt
import pandas as pd

def last_month_end():
    td = dt.datetime.today()
    enddt = dt.date(td.year, td.month-1, cal.monthrange(td.year, td.month-1)[1])
    return(enddt)

def date_days_ago(days=0):
    td = dt.datetime.today()
    tmpd = td - dt.timedelta(days=days)

    return str(tmpd.date())
