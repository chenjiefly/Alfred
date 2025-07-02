#!/usr/bin/python
# encoding: utf-8
import logging
import logging.handlers
import datetime
import traceback

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

rf_handler = logging.handlers.TimedRotatingFileHandler('./log/aliProductivity.log', when='midnight',  backupCount=3,encoding='utf-8')
rf_handler.setFormatter(logging.Formatter(LOG_FORMAT))

f_handler = logging.handlers.TimedRotatingFileHandler('./log/error.log',  when='midnight',  backupCount=3,encoding='utf-8')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)

def error(msg , extra={}):
    s = traceback.format_exc()
    logging.error("{} : {}".format(msg,s), extra=extra)

def info(msg , extra={}):
    logging.info(msg, exc_info=True, extra=extra)


if __name__ == '__main__':
    error("1234")
