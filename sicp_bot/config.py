from typing import Set, Dict

from sicp_bot.utils import Singleton
from sicp_bot.logger import get_logger

logger = get_logger(__name__)


class Config(metaclass=Singleton):
    def __init__(self, **kwargs: Dict[str, str]):
        for key in Config.keys():
            setattr(self, key, kwargs[key])
            logger.info(f'Set a config key: {key}')

    @staticmethod
    def keys() -> Set[str]:
        return {'CERT', 'DEBUG', 'DIR_PATTERN', 'GITHUB_TOKEN', 'HOST', 'ISSUER_ID', 'KEY', 'LISTEN', 'TELE_TOKEN'}
