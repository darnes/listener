import sys, os
import  logging
import logging.config
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

logging.config.fileConfig('./logging.conf')



from util.config import config
from util.oanda_utils import listen_and_report
# from util.oanda_utils import listen_and_log

log = logging.getLogger(__name__)

def main():
    log.info('starting')
    # next line to fail
    t = 12 / 0
    listen_and_report()
    # listen_and_log()

if __name__ == '__main__':
    main()
