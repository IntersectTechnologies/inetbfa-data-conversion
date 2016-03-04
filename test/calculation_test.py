from datamanager.envs import *
from datamanager.adjust import *
import pandas as pd

def test_backwards_calc():
    '''
    '''

def test_adjusted_close():
    # Import closing price data with pandas
    cp = path.join(MERGED_PATH, "Close.csv")
    dp = path.join(MERGED_PATH, "Dividend Ex Date.csv")
    close = pd.read_csv(cp, index_col = 0, parse_dates=True)
    divs = pd.read_csv(dp, index_col = 0, parse_dates=True)

    assert isinstance(close, pd.DataFrame)
    assert isinstance(divs, pd.DataFrame)