import sys
import  logging
import logging.config

logging.config.fileConfig('./logging.conf')


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
