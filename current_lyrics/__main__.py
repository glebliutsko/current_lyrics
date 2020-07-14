if not __package__:
    from os.path import dirname, abspath
    import sys
    path = abspath(__file__)
    sys.path.insert(0, dirname(dirname(path)))

import logging
from current_lyrics.app import App


def main():
    logger = logging.getLogger('yandex_music')
    logger.setLevel(logging.ERROR)

    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
