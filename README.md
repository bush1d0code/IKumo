# IKumo

POC of getting all Apple devices asociated with an account.
It will return data such as: Device Name, Device Model, Battery % and Location (Google Map URL)

P.S: Even if 2FA is activated on the account, it will be displaying the data.

## Single Password:
```bash
python3 i-kumo.py --appleid example@mail.com --password Password123
```

## Dictionary:
```bash
python3 i-kumo.py --appleid example@mail.com --password-list dictionary.txt
```
