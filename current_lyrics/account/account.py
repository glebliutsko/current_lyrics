from yandex_music import Client


class Account:
    def __init__(self, login, *, token=None, password=None):
        self.login = login
        if token:
            self.token = token
        elif password:
            ym = Client()
            self.token = ym.generate_token_by_username_and_password(login, password)
        else:
            raise ValueError()

    def to_dict(self):
        return {
            'login': self.login,
            'token': self.token
        }
