from typing import Dict

from sicp_bot.config import Config, config_fields


def test_config(mock_config_dict: Dict[str, str]):
    config = Config(
        **{
            key: value
            for (key, value) in mock_config_dict.items()
            if key in config_fields
        }
    )
    for field in config_fields:
        assert getattr(config, field) == mock_config_dict[field]
