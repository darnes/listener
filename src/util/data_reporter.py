import logging
import os
from v20.pricing import  ClientPrice
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb.resultset import ResultSet
from  datetime import datetime, timedelta
from enum import Enum
from typing import Generator
from .config import config

log = logging.getLogger(__name__)
INFLUX_HOST = os.environ.get('INFLUX_HOST', 'localhost')


class Symbol(Enum):
    JPY = 'USD_JPY'
    GBP = 'EUR_USD'
    EUR = 'GBP_USD'
    AUD = 'AUD_USD'
    GOLD = 'XAU_USD'
    BTC = 'BTC_USD'
    CORN = 'CORN_USD'
    WHEAT = 'WHEAT_USD'
    NAS100_USD = 'NAS100_USD'

    @classmethod
    def all_values(cls, glue: str = ','):
        return glue.join(
            map(lambda x: x.value, cls)
            )

class DataConnection(object):
    def __init__(self, url, token, org):
        self._client = InfluxDBClient(
            url=url, token=token, org=org
        )
        log.info('connected')


class DataReporter(DataConnection):
    def __init__(self, url, token, org):
        super().__init__(url, token, org)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)

    def report(self, price: ClientPrice):
        json_body = [
            {
                "measurement": 'price',
                "tags": {
                    "instrument": price.instrument,
                },
                "time": price.time,
                "fields": {
                    "bid": price.bids[0].price,
                    "ask": price.asks[0].price,
                }
            }
        ]
        self._write_api.write(bucket='tsdata', record=json_body)
        # self._write_api.flush()
        log.info('data sent')

def get_data_reporter():
    return DataReporter(
        config.influx_url,
        config.influx_token,
        config.influx_org
    )

class PricePoint(object):
    def __init__(self, time: datetime, bid: float, ask: float) -> None:
        self.time = time
        self.bid = bid
        self.ask = ask

    def __str__(self) -> str:
        return '{time}:\t{bid}\t{ask}'.format(time=self.time, bid=self.bid, ask=self.ask)

class DataReader(DataConnection):
    def day_data(self, date_str: str, symbol: Symbol) -> Generator[PricePoint, None, None]:
        dt = datetime.fromisoformat(date_str)
        start = dt
        end = start + timedelta(days=1)
        yield from self.get_data_stream(start, end, symbol)

    def week_data(self, date_str: str, symbol: Symbol) -> Generator[PricePoint, None, None]:
        dt = datetime.fromisoformat(date_str)
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)
        yield from self.get_data_stream(start, end, symbol)

    def get_result_set(self, symbol: Symbol, start: datetime, end: datetime, limit=100) -> ResultSet:
        return self._client.query("""
            SELECT "bid", "ask", "instrument" FROM "price" 
                WHERE "instrument" = '{symbol}' AND
                time > '{start}Z' and time < '{end}Z'
            ORDER BY time ASC
            LIMIT {limit}
            """.format(limit=limit, symbol=symbol.value, start=start.isoformat(), end=end.isoformat()),
            # chunked=True, chunk_size=10 chunked some sort of bullshit, chunking manually via start
        )

    def get_data_stream(self, start: datetime, end: datetime, symbol: Symbol) -> Generator[PricePoint, None, None]:
        log.info('data from %s till %s', start, end)
        current_start = start
        has_more = True
        while has_more and current_start < end:
            log.debug('getting next chunk %s', current_start)
            results = self.get_result_set(symbol, current_start, end, limit=100)
            has_more = False
            for point in results.get_points(tags={'instrument': symbol.value}):
                dt = datetime.fromisoformat(point['time'][:-1])
                current_start = dt
                yield PricePoint(dt, point['bid'], point['ask'])
                has_more = True

