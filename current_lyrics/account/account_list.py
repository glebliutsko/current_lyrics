import json
import os

from current_lyrics.account import Account


class AccountList:
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(self.filename):
            pass

        self.accounts = list()

    def add(self, login, token):
        self.accounts.append(Account(login, token=token))

    def add_by_password(self, login, password):
        self.accounts.append(Account(login, password=password))

    def to_list(self):
        return [i.to_dict() for i in self.accounts]

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.to_list(), f, indent=0)

    def _read(self):
        with open(self.filename, 'r') as f:
            try:
                parsed_json = json.load(f)
                for i in parsed_json:
                    self.accounts.append(Account(i['login'], token=i['token']))
            except json.decoder.JSONDecodeError:
                print('Invalid config file')
            except KeyError:
                print('Invalid config file')
