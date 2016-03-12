import numpy as np
import pandas as pd
from os import path

dir = path.dirname(__file__)
TESTDATA = pd.read_csv(path.join(dir, 'TEST.csv'), index_col = 0, parse_dates = True)
