from datetime import datetime, timedelta
from urllib import response
import boto3
import logging
import threading

"""
IMPORTANT: switch to CLoudWatch Agent
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-open-telemetry.html
"""

log = logging.getLogger(__name__)

REPORT_INTERVAL = timedelta(seconds=30)

class AgregatedReporter(object):
    def __init__(self, metric_name: str) -> None:
        self.client = boto3.client('cloudwatch')
        self._last_report = datetime.utcnow()
        self._value = 0
        self._metric_name = metric_name
        self._last_thread = None

    def _report(self):
        if datetime.utcnow() - self._last_report > REPORT_INTERVAL:
            self._send_report_data(self._value)
            self._value = 0
            self._last_report  = datetime.utcnow()

    @staticmethod
    def _send_report_async(client, metric_name, value):
        client.put_metric_data(
        Namespace='Listener', # todo: make it configurable
        MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': [
                        {
                            'Name': 'DefaultDimensionName',
                            'Value': 'DefaultDimensionValue'
                        }
                    ],
                    'Value': value,
                    'Unit': 'Count'
                },
            ]
        )
    def _send_report_data(self, value: int):
        if self._last_thread is not None:
                self._last_thread.join()
        log.info('sending counter value', extra={'value': value})
        self._last_thread = threading.Thread(
            target=self._send_report_async,
            args=(self.client, self._metric_name, value, )
        )
        self._last_thread.start()

    def inc(self):
        self._value += 1
        self._report()
    
    

reporter = AgregatedReporter('NumberOfMessages')

def incr_message_counter():
    reporter.inc()

