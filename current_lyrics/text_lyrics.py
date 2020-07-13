import tkinter as tk


class TextLyrics(tk.Text):
    def __init__(self):
        super().__init__(state=tk.DISABLED)

    def update_lyrics(self, lyrics: str):
        """Обновляет текст"""
        self.configure(state=tk.NORMAL)
        self.delete('0.0', tk.END)
        self.insert(tk.END, lyrics)
        self.configure(state=tk.DISABLED)
