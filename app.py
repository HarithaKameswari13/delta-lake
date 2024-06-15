from prometheus_client import start_http_server, Summary, Counter, Gauge
import random
import time


REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter('request_count', 'Number of requests')
IN_PROGRESS = Gauge('in_progress_requests', 'In progress requests')

@REQUEST_TIME.time()
def process_request(t):

    IN_PROGRESS.inc()
    time.sleep(t)
    IN_PROGRESS.dec()
    REQUEST_COUNT.inc()

if __name__ == '__main__':

    start_http_server(8000)

    while True:
        process_request(random.random())
