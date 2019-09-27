from dataclasses import dataclass, fields

from sicp_bot.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Config:
    CERT: str
    DEBUG: str
    DIR_PATTERN: str
    GITHUB_TOKEN: str
    HOST: str
    ISSUER_ID: str
    KEY: str
    LISTEN: str
    TELE_TOKEN: str


config_fields = [field.name for field in fields(Config)]
