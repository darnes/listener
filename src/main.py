import sys
import logging
# doing this here, so config can log as others
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s\t:%(name)s:[%(asctime)s]:%(message)s')

from util.config import config
from util.oanda_utils import listen_and_log

log = logging.getLogger(__name__)
#todo: consider adding DT to traceback


def main():
    log.info('starting')
    listen_and_log()

if __name__ == '__main__':
    main()
