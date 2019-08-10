from dataclasses import dataclass
from typing import List

from src.config import Config
import re

_DIR_SPLIT_SYM = '/'


@dataclass
class ParsePattern:
    username: str
    repo: str
    leaf_file: str
    folder_structure: List[str]


def _pattern_validator(dir_pattern: str) -> ParsePattern:
    from collections import deque
    try:
        patterns = dir_pattern.split(_DIR_SPLIT_SYM)

        try:
            deque(map(lambda pattern: re.compile(pattern), patterns), maxlen=0)
        except re.error as e:
            raise Exception("One of the patterns is incompatible!", e)

        username, repo, *files = patterns
        leaf_file, *reverse_structure = files[::-1]
        folder_structure = reverse_structure[::-1]

        return ParsePattern(
            username=username,
            repo=repo,
            leaf_file=leaf_file,
            folder_structure=folder_structure
        )
    except ValueError as e:
        raise Exception("Not compatible directory pattern!", e)


def get_parser(config: Config) -> ParsePattern:
    return _pattern_validator(config.DIR_PATTERN)
