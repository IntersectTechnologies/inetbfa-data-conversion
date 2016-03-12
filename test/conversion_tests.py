from datamanager.utils import last_month_end
from mock_data import TESTDATA
import numpy as np

def test_last_date_of_conversion():
    
    select = TESTDATA.index[TESTDATA.index > np.datetime64(last_month_end())]

    assert len(select) == 0
