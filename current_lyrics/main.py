import logging
import tkinter as tk
import typing

import yandex_music

from current_lyrics.text_lyrics import TextLyrics
from current_lyrics.title_track import TitleTrack
from current_lyrics.account_menu import AccountMenu
from current_lyrics.add_account_window import AddAccountWindow
from current_lyrics.account import AccountList

logger = logging.getLogger('yandex_music')
logger.setLevel(logging.ERROR)


class LastTrack(typing.NamedTuple):
    index: int
    queues_id: str


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.time_update_ms = 1000

        # Label с назаванием трека
        self.title_track_label = TitleTrack()
        self.title_track_label.pack()

        # TextBox с текстом трека
        self.lyrics_text = TextLyrics()
        self.lyrics_text.pack(expand=True, fill=tk.BOTH)

        self.accounts = AccountList('./account.json')

        # Option Menu со списком аккаунтов
        self.account_menu = AccountMenu(self, self.accounts, command=self.yandex_music_client_reinitialize)
        self.account_menu.pack(side=tk.LEFT)

        # Button для добавления аккаунта
        self.button_add = tk.Button(self, text='Добавить аккаунт')
        self.button_add.bind('<Button-1>', self.account_add)
        self.button_add.pack()

        self.title("Текст текущего трека")

        self.last_track: LastTrack or None = None

        # Если аккаунтов нет, то предлагаем пользователю добавить новый аккаунт
        if len(self.accounts) == 0:
            self.account_add()

        self.ym = None
        self.yandex_music_client_reinitialize()

        self.update_track()

    def yandex_music_client_reinitialize(self, *args, **kwargs):
        # Иногда, функция может быть вызвана еще до полной инициализации account_menu.
        if not hasattr(self, 'account_menu'):
            return

        token = self.account_menu.get_token()
        if token is not None:
            self.ym = yandex_music.Client(token)
        else:
            self.ym = None

    def account_add(self, *args, **kwargs):
        """Вызывает окно, для добавления нового аккаунта"""
        AddAccountWindow(self.accounts, self.account_menu.update_accounts)

    def destroy(self):
        self.accounts.save()
        super().destroy()

    def update_track(self):
        """Обновляет слова в self.lyrics_text"""
        if self.ym is not None:
            # Получение всех очередей.
            queues = self.ym.queues_list()
            # Последняя обновленная очередь всегда самая первая в списке.
            current_queues_id = queues[0].id

            # Получаем полную информацию о очереде.
            current_queues = self.ym.queue(current_queues_id)
            current_track_index = current_queues.current_index

            # Проверяем, переключился ли трек
            if not self.last_track or \
                    (self.last_track.index != current_track_index or self.last_track.queues_id != current_queues_id):
                # Получаем сокращенную информацию о треке
                current_track_short = current_queues.tracks[current_track_index]
                # Формируем полный ID в формате 'track_id:album_id' и получаем полную информацию о треке
                current_track = self.ym.tracks(f'{current_track_short.track_id}:{current_track_short.album_id}')[0] \
                    if current_track_short.album_id else self.ym.tracks(current_track_short.track_id)[0]

                # Обновляем название трека в окне
                self.title_track_label.set_title(current_track.title, current_track.artists[0].name)

                lyrics_text = current_track.get_supplement().lyrics
                if lyrics_text:
                    self.lyrics_text.update_lyrics(lyrics_text.full_lyrics)
                else:
                    self.lyrics_text.update_lyrics('Слова не найдены')

                self.last_track = LastTrack(index=current_track_index, queues_id=current_queues_id)

        self.after(self.time_update_ms, self.update_track)


if __name__ == '__main__':
    app = App()
    app.mainloop()
