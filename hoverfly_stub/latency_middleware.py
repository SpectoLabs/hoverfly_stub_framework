#!/usr/bin/env python
import sys
import os
import logging
from time import sleep
import pandas as pd
import json
import re


# File names
log_file_name = 'stub_latency_middleware.log'
latency_csv_name = 'API_Collection_and_Latency.csv'

# Path Locations
proj_path = os.path.abspath(os.path.dirname(__file__))
# latency_csv_path = os.path.join(proj_path, "API_Collection_and_Latency.csv")

# Logging
logging.basicConfig(filename="stub_middleware.log", level=logging.DEBUG)
logging.debug('latency_middleware is called')

# Reading CSV to Dataframe
logging.debug('Reading Latency csv')
latency_df = pd.read_csv("API_Collection_and_Latency.csv")


# Main
def main():

    data = sys.stdin.readlines()
    # this is a json string in one line so we are interested in that one line
    payload = data[0]
    # payload = '{"response":{"status":200,"body":"ok","encodedBody":false,"headers":{"test_header":["true"]}},"request":{"path":"/core/23456/connect/token","method":"GET","destination":"www.test.com","scheme":"","query":"","body":"","headers":{"test_header":["true"]}}}'

    # Read Payload
    payload_json_dict = json.loads(payload)

    # Get payload request path
    payload_req_path = payload_json_dict['request']['path']

    request_found = False
    # Match the request path with csv
    for index, row in latency_df.iterrows():
        pattern = re.compile(latency_df['Path'][index])
        if pattern.match(payload_req_path):
            request_found = True
            set_latency = latency_df['Latency'][index]

    # Set Latency
    if request_found:
        # Set delay
        logging.debug("Request {} found, setting latency to {} sec(s)".format(payload_req_path, set_latency))
        LINK_REQ_RESPONSE_TIME = set_latency
    else:
        logging.debug("API_Collection_and_Latency.csv doesn't have request - {}".format(payload_req_path))
        logging.debug("Setting Link Response Time to default value of .5 secs".format(payload_req_path))
        # Set delay
        LINK_REQ_RESPONSE_TIME = 0.5

    logging.debug("sleeping for {} second(s)".format(LINK_REQ_RESPONSE_TIME))

    # Convert
    sleep(LINK_REQ_RESPONSE_TIME)

    # do not modifying payload, returning same one
    print(payload)


if __name__ == "__main__":
    main()
