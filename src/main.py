import sys, os
import  logging
import logging.config

logging.config.fileConfig('./logging.conf')

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

from util.config import config
# from util.oanda_utils import listen_and_report
from util.oanda_utils import listen_and_log

log = logging.getLogger(__name__)

def main():
    log.info('starting')
    # listen_and_report()
    listen_and_log()

if __name__ == '__main__':
    main()
