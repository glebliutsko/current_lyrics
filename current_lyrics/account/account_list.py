import json
import os
import typing

from current_lyrics.account import Account


class AccountNotFound(Exception):
    pass


class AccountList:
    def __init__(self, filename):
        self.accounts: typing.List[Account] = list()

        self.filename = filename
        if os.path.exists(self.filename):
            self._read()

    def get_token(self, login: str) -> str:
        """Возвращает токен для аккаунта с логином == login"""
        for account in self.accounts:
            if account.login == login:
                return account.token

        raise AccountNotFound

    def get_list_name_account(self) -> typing.List[str]:
        """Список login'ов всех аккаунтов"""
        return [i.login for i in self.accounts]

    def add(self, login, token):
        """Добавляет аккаунт по login и token"""
        self.accounts.append(Account(login, token=token))

    def add_by_password(self, login, password):
        """Добавляет аккаунт по логину (login) и паролю (password)"""
        self.accounts.append(Account(login, password=password))

    def to_list(self) -> typing.List[dict]:
        return [i.to_dict() for i in self.accounts]

    def save(self):
        """Сохраняет в файл"""
        with open(self.filename, 'w') as f:
            json.dump(self.to_list(), f, indent=0)

    def _read(self):
        """Читает файл"""
        with open(self.filename, 'r') as f:
            try:
                parsed_json = json.load(f)
                for i in parsed_json:
                    self.accounts.append(Account(i['login'], token=i['token']))
            except json.decoder.JSONDecodeError:
                print('Invalid config file')
            except KeyError:
                print('Invalid config file')

    def __len__(self):
        return len(self.accounts)
