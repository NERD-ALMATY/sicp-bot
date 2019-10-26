from setuptools import setup

setup(
    name="sicp-bot",
    version="0.2.0",
    description="Simple SICP leaderboard telegram bot. ",
    author="nerd-iitu",
    author_email="arpanetus@protonmail.com",
    url="https://github.com/nerd-iitu/sicp-bot",
    packages=["sicp_bot"],
    license="NPOSL3.0",
    install_requires=[
        "jsons==0.10.2",
        "Flask-RESTful==0.3.7",
        "plyvel==1.1.0",
        "PyGithub==1.43.8",
        "pyTelegramBotAPI==3.6.6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Environment :: Console",
    ],
    scripts=["bin/sicp-bot"],
)
