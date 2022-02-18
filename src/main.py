import sys
import time
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s\t:%(name)s:[%(asctime)s]:%(message)s')
log = logging.getLogger(__name__)


def main():
    log.info('starting')
    countdown = 10
    while True:
        time.sleep(1.0)
        log.info('info beep')
        log.debug('debug beep')
        log.warning('warning beep')
        log.error('error beep')
        countdown -= 1
        log.info('1/countdown %s', 1 / countdown)

if __name__ == '__main__':
    main()
