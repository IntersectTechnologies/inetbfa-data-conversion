from os import path, listdir
import re, codecs
import logging

import datamanager.tasks as tasks
# logging

logger = logging.getLogger('datamanager')
formatter = logging.Formatter("'%(asctime)s-%(name)s-%(levelname)s - %(message)s'")

fileHandler = logging.FileHandler("{0}.log".format('datamanager'))
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

logger.info('Initializing data processing')
tasks.task_startup()

log.info('Start converting data')
tasks.task_convert_ref_data()
tasks.task_convert_market_data()

tasks.task_merge_ref_data()
tasks.task_merge_market_data()

logging.info('Calculating adjusted close')
tasks.task_calc_adjusted_close()

logging.info('Syncing data to all registered slaves')
tasks.task_sync_data()

logging.info('Updating NWU Momentum Portfolio')
tasks.task_update_nwu_momentum_portfolio()
    
