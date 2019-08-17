from dataclasses import dataclass

import re


@dataclass
class ParsePattern:
    dir_pattern: str


def _pattern_validator(dir_pattern: str) -> ParsePattern:
    try:
        re.compile(dir_pattern)

        return ParsePattern(
            dir_pattern
        )
    except ValueError as e:
        raise Exception('Not compatible directory pattern!', e)


def get_parser(dir_pattern: str) -> ParsePattern:
    return _pattern_validator(dir_pattern)
