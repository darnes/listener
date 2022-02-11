import sys
import time
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(levelname)s\t:%(name)s:[%(asctime)s]:%(message)s')
log = logging.getLogger(__name__)


def main():
    log.info('starting')
    while True:
        time.sleep(1.0)
        log.info('info beep')
        log.debug('debug peep')
        log.warn('warn peep')
        log.error('error peep')

if __name__ == '__main__':
    main()
