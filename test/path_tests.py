from os import path
from datamanager.envs import *

def test_paths():
    assert path.exists(DATA_ROOT)
    assert path.exists(DL_PATH)
    assert path.exists(MASTER_DATA_PATH)
    assert path.exists(CONVERT_PATH)
    assert path.exists(MERGED_PATH)