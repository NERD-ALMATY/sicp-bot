from os import environ as env_dict
from pathlib import Path

from typing import Dict, Any

_data_path = "{}/{}/".format(Path(__file__).parent.parent, "data")


def get_data_folder_path() -> str:
    return _data_path


class Singleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
