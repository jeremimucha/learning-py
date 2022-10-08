# Commandline tools to manage the backend


## Creating users

The `create_super_user.py` creates an admin user with the given credentials.
Make sure to extend the PYTHONPATH first, before running the script, so that the imports work.

```bash
$ python .\create_super_user.py -f Test -l Admin -e admin@testmail.com -p 123456789 -iban PL10105000997603123456789123 -ps 1234
```
