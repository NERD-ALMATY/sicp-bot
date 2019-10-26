import pytest

from sicp_bot import get_parser


def test_get_parser(parse_pattern):
    assert get_parser("(?s).*") == parse_pattern


def test_fail_get_parser():
    with pytest.raises(Exception):
        assert get_parser("[")
