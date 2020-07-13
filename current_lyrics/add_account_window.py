import tkinter as tk
import tkinter.messagebox

import yandex_music.exceptions

from current_lyrics.account import AccountList


class AddAccountWindow(tk.Toplevel):
    def __init__(self, accounts: AccountList, callback_account_add=None):
        super().__init__()
        self.callback_account_add = callback_account_add
        self.accounts = accounts

        self.attributes('-type', 'dialog')

        self.login = tk.Entry(self)
        self.login.pack()

        self.password = tk.Entry(self, show='*')
        self.password.pack()

        self.button = tk.Button(self, text='Добавить')
        self.button.bind('<Button-1>', self.add)
        self.button.pack()

        self.title('Добавление аккаунта')

    def add(self, event):
        login: str = self.login.get()
        password: str = self.password.get()

        try:
            self.accounts.add_by_password(login, password)

            if self.callback_account_add is not None:
                self.callback_account_add()

            self.destroy()
        except yandex_music.exceptions.BadRequest:
            tk.messagebox.showerror('Ошибка', 'Неверный логин или пароль')
