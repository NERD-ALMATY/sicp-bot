from pathlib import Path

from typing import Dict, Any

_data_path = f"{Path(__file__).parent.parent}/{'data'}/"


def get_data_folder_path() -> str:
    return _data_path


default_message_texts = {
    'start_text': """ Hey, cowboy! Happy to see ya!
This bot was created in order to involve people in solving SICP exercises with fun. 

Here are the commands you can run:
/start - show this message.
/help - show this message.
/get {username} - get user profile.
/leaderboard [size] - get leaderboard with size.

If you are an admin:
/add - add new user(follow the messages).
/del - del existing user(follow the messages).

Hope you're going to enjoy using it!
maintainer: @arpanetus
repository: [github.com/nerd-iitu/sicp-bot](https://github.com/nerd-iitu/sicp-bot)
""",

    'add_msg_text': """Here's the syntax to add:
username: arpanetus
name: arpanetus
repo: sicp-ans
""",

    'del_msg_text': """Simply place the username:
arpanetus
"""
}


class Singleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
