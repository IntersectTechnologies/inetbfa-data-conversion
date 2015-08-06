﻿from os import path, listdir
import re, codecs
import logging
import sys
import datamanager.tasks as tasks
from core.utils import getLog

log = getLog('datamanager')

log.info('Initializing data processing')
tasks.task_startup()

log.info('Starting to convert data')
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
    
