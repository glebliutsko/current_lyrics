import tkinter as tk

import typing

from current_lyrics.account import AccountList


class AccountMenu(tk.OptionMenu):
    def __init__(self, root: tk.Tk, accounts: AccountList, command, **kwargs):
        self.var = tk.StringVar()
        # Callback при изменении аккаунта
        self.var.trace('w', command)

        self.accounts = accounts
        account_list = self.accounts.get_list_name_account()

        if len(account_list) > 0:
            super().__init__(root, self.var, *account_list, **kwargs)
            self.var.set(account_list[0])
        else:
            super().__init__(root, self.var, '-', command=command, **kwargs)

    def update_accounts(self):
        """Сихронизирует со списоком аккаунтов"""
        # https://stackoverflow.com/a/17581364/11465354
        self['menu'].delete(0, tk.END)

        account_list = self.accounts.get_list_name_account()
        if len(account_list) > 0:
            for i in account_list:
                self['menu'].add_command(label=i, command=tk._setit(self.var, i))
        else:
            self['menu'].add(label='-')

    def get_token(self) -> typing.Union[str, None]:
        """Возвращает токен выбраного аккаунта. Если аккаунт не выбран, то возвращает None"""
        if self.var.get() in ('-', ''):
            return None

        return self.accounts.get_token(self.var.get())
