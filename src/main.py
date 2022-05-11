import sys
import logging
# doing this here, so config can log as others
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s:%(name)s:[%(asctime)s]:%(message)s')

from util.config import config
from util.oanda_utils import listen_and_report

from util.data_reporter import DataConnection

log = logging.getLogger(__name__)

def main():
    log.info('starting')
    listen_and_report()

if __name__ == '__main__':
    main()
