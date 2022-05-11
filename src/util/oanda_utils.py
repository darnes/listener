import logging
import time

import v20
from v20.errors import V20ConnectionError, V20Timeout

from .config import config
from .data_reporter import get_data_reporter, DataReporter, Symbol


log = logging.getLogger(__name__)

def get_stream_api():
    log.info('stream host name %s', config.OANDA_STREAM_HOST_NAME)
    ctx = v20.Context(
        hostname=config.OANDA_STREAM_HOST_NAME,
        token=config.OANDA_TOKEN,
    )
    return ctx

def get_rest_api():
    ctx = v20.Context(
        hostname=config.OANDA_REST_HOST_NAME,
        token=config.OANDA_TOKEN,
    )
    return ctx

def price_to_string(price):
    return "{} ({}) {}/{}".format(
        price.instrument,
        price.time,
        price.bids[0].price,
        price.asks[0].price
    )

def heartbeat_to_string(heartbeat):
    return "HEARTBEAT ({})".format(
        heartbeat.time
    )

def unsafe_listen_and_log():
    api = get_stream_api()
    stream = api.pricing.stream(
        accountID=config.OANDA_ACCOUNT_ID,
        instruments=Symbol.all_values(),
        snapshot=True
    )
    log.info('printing messages as they appear')
    for msg_type, msg in stream.parts():
        log.info('got message %s', msg_type)
        if msg_type == "pricing.PricingHeartbeat":
            log.info(heartbeat_to_string(msg))
        elif msg_type == "pricing.ClientPrice":
            log.info(price_to_string(msg))

def listen_and_log():
    while True:
        try:
            log.info('starting read_and_log')
            unsafe_listen_and_log()
        except (V20ConnectionError, V20Timeout) as v20_error:
            log.error('V20Error: %s', v20_error)
            log.info('sleeping for 3 seconds to reconnect')
            time.sleep(3)

def unsafe_listen_and_report():
    api = get_stream_api()
    stream = api.pricing.stream(
        accountID=config.OANDA_ACCOUNT_ID,
        instruments=Symbol.all_values(),
        snapshot=True
    )
    dr = get_data_reporter()

    log.info('printing messages as they appear')
    for msg_type, msg in stream.parts():
        log.info('got message %s', msg_type)
        if msg_type == "pricing.PricingHeartbeat":
            log.info(heartbeat_to_string(msg))
        elif msg_type == "pricing.ClientPrice":
            log.info(price_to_string(msg))
            dr.report(price=msg)

def listen_and_report():
    while True:
        try:
            log.info('starting listen_and_report')
            unsafe_listen_and_report()
        except (V20ConnectionError, V20Timeout) as v20_error:
            log.error('V20Error: %s', v20_error)
            log.info('sleeping for 3 seconds to reconnect')
            time.sleep(3)