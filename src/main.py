import sys, os
import  logging
import logging.config
import traceback
from types import TracebackType

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

logging.config.fileConfig('./logging.conf')
from watchtower import CloudWatchLogHandler


from util.config import config
from util.oanda_utils import listen_and_report
from util.oanda_utils import listen_and_log

log = logging.getLogger(__name__)

def handle_exception(exc_type, exc_value, exc_tb):
    log.critical('uncaugh-exception', exc_info=(exc_type, exc_value, exc_tb))
sys.excepthook = handle_exception

"""
cloudWatch logs insights:
fields @timestamp, @message, levelname
| filter levelname = "CRITICAL"
| sort @timestamp desc
| limit 20

"""

def main():
    log.info('starting')
    listen_and_report()
    # listen_and_log()

if __name__ == '__main__':
    main()
