import os

import requests
import pandas as pd
from datetime import datetime

# Prometheus endpoint
PROMETHEUS_URL = 'http://localhost:9090/api/v1/query'

# Metrics to query
metrics = [
    'request_processing_seconds_sum',
    'request_processing_seconds_count',
    'request_count',
    'in_progress_requests'
]

data = []

for metric in metrics:
    print(f"Querying metric: {metric}")
    response = requests.get(PROMETHEUS_URL, params={'query': metric})
    if response.status_code == 200:
        result = response.json()['data']['result']
        for r in result:
            timestamp, value = r['value']
            timestamp = datetime.fromtimestamp(int(timestamp))
            data.append([metric, timestamp, value])
    else:
        print(f"Failed to query metric: {metric}, status code: {response.status_code}")

if data:
    df = pd.DataFrame(data, columns=['metric', 'timestamp', 'value'])
    # Export to CSV
    # Check if the file exists
    file_exists = os.path.isfile('metrics.csv')

    # Append to existing CSV file if it exists, otherwise create a new file
    mode = 'a' if file_exists else 'w'
    header = not file_exists

    # Export to CSV
    df.to_csv('metrics.csv', mode=mode, header=header, index=False)
    print("CSV file created successfully.")
else:
    print("No data to write to CSV.")
