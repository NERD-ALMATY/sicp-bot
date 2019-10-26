from sicp_bot import get_parser


# TODO: add failing case too


def test_get_parser(parse_pattern):
    assert get_parser("(?s).*") == parse_pattern
