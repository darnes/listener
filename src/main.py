import sys
import time
import logging

import v20
from v20.errors import V20ConnectionError, V20Timeout
from util.data_reporter import DataReporter, Symbol


logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s\t:%(name)s:[%(asctime)s]:%(message)s')
log = logging.getLogger(__name__)
#todo: consider adding DT to traceback

def main():
    log.info('starting')
    countdown = 10
    while True:
        time.sleep(1.0)
        log.info('info beep with oanda')
        log.debug('debug beep with oanda')
        log.warning('warning beep')
        log.error('error beep')
        countdown -= 1
        log.info('1/countdown %s', 1 / countdown)

if __name__ == '__main__':
    main()
