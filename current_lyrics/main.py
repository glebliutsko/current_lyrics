import logging
import os
import sys
import tkinter as tk

import yandex_music

from current_lyrics.text_lyrics import TextLyrics
from current_lyrics.title_track import TitleTrack

logger = logging.getLogger('yandex_music')
logger.setLevel(logging.ERROR)

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print('Usage: TOKEN=token main.py')
    sys.exit()


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ym = yandex_music.Client(TOKEN)
        self.time_update_ms = 1000

        self.title_track_label = TitleTrack()
        self.title_track_label.pack()

        self.lyrics_text = TextLyrics()
        self.lyrics_text.pack(expand=True, fill=tk.BOTH)

        self.title = 'Current Lyrics'

        self.update()

    def update(self):
        queues = self.ym.queues_list()

        current_queues_id = queues[0].id
        current_queues = self.ym.queue(current_queues_id)

        current_track_index = current_queues.current_index
        current_track_id = current_queues.tracks[current_track_index]
        current_track = self.ym.tracks(f'{current_track_id.track_id}:{current_track_id.album_id}')[0] \
            if current_track_id.album_id else self.ym.tracks(current_track_id.track_id)[0]

        self.title_track_label.set_title(current_track.title, current_track.artists[0].name)
        lyrics_text = current_track.get_supplement().lyrics
        if lyrics_text:
            self.lyrics_text.update_lyrics(lyrics_text.full_lyrics)
        else:
            self.lyrics_text.update_lyrics('Слова не найдены')

        self.after(self.time_update_ms, self.update)


if __name__ == '__main__':
    app = App()
    app.mainloop()
