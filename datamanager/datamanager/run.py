from os import path, listdir
import re, codecs
import logging

import datamanager.tasks as tasks
from core.utils import getLog
# logging


def main():
    log = getLog('datamanager')
    log.info('Initializing data processing')
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
    

if __name__ == "__main__":
    main()