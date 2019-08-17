from typing import Set, Dict

from sicp_bot.utils import Singleton


class Config(metaclass=Singleton):
    def __init__(self,**kwargs: Dict[str, str]):
        for key in Config.keys():
            setattr(self, key, kwargs[key])

    @staticmethod
    def keys() -> Set[str]:
        return {'CERT', 'DEBUG', 'DIR_PATTERN', 'GITHUB_TOKEN', 'HOST', 'ISSUER_ID', 'KEY', 'LISTEN', 'TELE_TOKEN'}
