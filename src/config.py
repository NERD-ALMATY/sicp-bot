from src.standards import Singleton


class Config(metaclass=Singleton):
    TELE_TOKEN: str
    GITHUB_TOKEN: str
    DIR_PATTERN: str

    def __init__(self, tele_token: str, github_token: str, dir_pattern: str):
        self.TELE_TOKEN = tele_token
        self.GITHUB_TOKEN = github_token
        self.DIR_PATTERN = dir_pattern
