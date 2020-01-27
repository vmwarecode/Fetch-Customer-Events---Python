#!/usr/bin/python3
#
# Fetch customer events over a long time horizon; navigate paginated result set.
# 
# Usage: VC_USERNAME='user@velocloud.net' VC_PASSWORD=s3cret python events.py
#

import os
from datetime import datetime, timedelta
from client import *

# EDIT THESE
VCO_HOSTNAME = 'vcoX.velocloud.net'
ENTERPRISE_ID = 1

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def main():

    client = VcoRequestManager(VCO_HOSTNAME)
    client.authenticate(os.environ['VC_USERNAME'], os.environ['VC_PASSWORD'], is_operator=os.environ.get('VC_OPERATOR', False))

    start_time = datetime.utcnow() - timedelta(days=10)
    end_time = datetime.utcnow()

    has_more = True
    events = []

    while has_more:
        result = client.call_api('event/getEnterpriseEvents', {
            'enterpriseId': ENTERPRISE_ID,
            'interval': {
                'start': start_time.strftime(DATE_FORMAT),
                'end': end_time.strftime(DATE_FORMAT)
            }
        })
        events += result['data']
        # Check evenTime on the oldest-reported event, and update the query end_time accordingly
        end_time = datetime.strptime(result['data'][-1]['eventTime'], DATE_FORMAT)
        has_more = result['metaData']['more']

    print('Found %d total events' % len(events))

if __name__ == '__main__':
    main()