import tkinter as tk


class TitleTrack(tk.Label):
    def __init__(self):
        super().__init__()

    def set_title(self, track: str, artist: str):
        full_title = f'{artist} — {track}'
        self.configure(text=full_title)
