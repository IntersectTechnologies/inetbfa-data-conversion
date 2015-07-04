import logging

__version__ = (0,1,0)

def init_logger():
    logger = logging.getLogger(__name__)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()

    fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)