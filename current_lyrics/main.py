import logging
import tkinter as tk
import typing

import yandex_music
import yandex_music.exceptions

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
            def get_current_queues() -> typing.Tuple[str, 'yandex_music.Queue']:
                """Получает текущую очередь"""
                current_queue = current_queues_id = None
                while not current_queue:
                    # Получение всех очередей.
                    queues = self.ym.queues_list()
                    # Последняя обновленная очередь всегда самая первая в списке.
                    current_queues_id = queues[0].id

                    # Иногда, очередь может обновится между получением списка очередей и получением полной информации
                    # о ней. Если это произошло, то повторяем получение ID.
                    try:
                        # Получаем полную информацию о очереде.
                        current_queue = self.ym.queue(current_queues_id)
                    except yandex_music.exceptions.BadRequest:
                        pass

                return current_queues_id, current_queue

            def get_new_track_data(track_id):
                """Получение информации (исполнитель, название, слова) о новом треке."""
                current_track = self.ym.tracks(track_id)[0]

                lyrics = current_track.get_supplement().lyrics
                if lyrics:
                    lyrics_text = lyrics.full_lyrics
                else:
                    lyrics_text = 'Слова не найдены'

                return current_track.title, current_track.artists[0].name, lyrics_text

            try:
                current_queues_id, current_queue = get_current_queues()
                current_track_index = current_queue.current_index

                # Проверяем, переключился ли трек
                if not self.last_track or \
                        (self.last_track.index != current_track_index or self.last_track.queues_id != current_queues_id):
                    # Получаем сокращенную информацию о треке
                    current_track_short = current_queue.tracks[current_track_index]

                    # Формируем ID трека в формате 'track_id:album_id'
                    track_id = current_track_short.track_id
                    if current_track_short.album_id:
                        track_id += f':{current_track_short.album_id}'

                    title, artists, lyrics = get_new_track_data(track_id)

                    # Обновляем информацию треке в окне
                    self.title_track_label.set_title(title, artists)
                    self.lyrics_text.update_lyrics(lyrics)

                    self.last_track = LastTrack(index=current_track_index, queues_id=current_queues_id)
            finally:
                self.after(self.time_update_ms, self.update_track)


if __name__ == '__main__':
    app = App()
    app.mainloop()
