import unittest
from datamanager.envs import *
from datamanager.adjust import *

class Test_datamanager(unittest.TestCase):
    def test_backwards_calc(self):
        '''
        '''
    
    def test_adjusted_close(self):
        # Import closing price data with pandas
        cp = path.join(MERGED_PATH, "Close.csv")
        dp = path.join(MERGED_PATH, "Dividend Ex Date.csv")
        close = pd.read_csv(cp, index_col = 0, parse_dates=True)
        divs = pd.read_csv(dp, index_col = 0, parse_dates=True)

        self.assertIsInstance(close, pd.DataFrame)
        self.assertIsInstance(divs, pd.DataFrame)

        #self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
