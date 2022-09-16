# IKumo

POC of getting all Apple devices with data such as: Device Name, Device Model, Battery % and Location (Google Map URL)
The only requirement is: having an Apple ID and Password (No 2FA required even if is enable on the account)

example of usage: 
Single Password:
python3 i-kumo.py --appleid example@mail.com --password Password123

Dictionary:
python3 i-kumo.py --appleid example@mail.com --password-list dictionary.txt
