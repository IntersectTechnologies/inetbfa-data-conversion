"""
Load data from Donwloaded Excel files and process them
"""

import argparse
from os import path, listdir
import re, codecs
import logging
import sys
import datamanager.tasks as tasks
from logbook import Logger, NestedSetup, RotatingFileHandler, StreamHandler

log = Logger(__name__)


def main(args):
    log.notice('Starting datamanager {version}...'.format(version=__version__))
    log.notice('Using arguments: %s' % args)

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

def parseArgs():
    """Parse CLI arguments using argparse and return NameSpace object"""
    parser = argparse.ArgumentParser("datamanager - \
        task runner for several data processing tasks",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("all", help="run all data processing tasks", default=1200, type=str)
    #parser.add_argument('--version', action='version', version='{0}'.format(__version__))

    args = parser.parse_args()
    return args

def enter():
    args = parseArgs()
    logFileName = os.path.join(args.directory, 'datamanager.log')
    log_setup = NestedSetup([
        RotatingFileHandler(logFileName),
        StreamHandler(sys.stdout, level='NOTICE', bubble=True,
            format_string='{record.message}')
        ])
    with log_setup.applicationbound():
        main(args)
    
if __name__=='__main__':
    enter()