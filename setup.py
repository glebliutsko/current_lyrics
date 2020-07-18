import os
import json

from setuptools import setup, find_packages


def requirements():
    """Создание листа зависимостей для этого проекта."""
    pipfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Pipfile.lock")
    with open(pipfile) as pip_file:
        pipfile_json = json.load(pip_file)

    return [
        package + detail.get("version", "")
        for package, detail in pipfile_json["default"].items()
    ]


setup(
    name="yandexlyrics",
    version="0.1",
    author="Gleb Liutsko",
    author_email="gleb290303@gmail.com",
    license="MIT",
    url="https://github.com/glebliutsko/current_lyrics",
    install_requires=[
        "yandex-music"
    ],
    dependency_links=[
        "git+https://github.com/MarshalX/yandex-music-api.git@134f3bcf0d68418dc14904cf165660c0a1d0eaca#egg=yandex-music"
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["yandexlyrics=yandexlyrics.__main__:main"]}
)
