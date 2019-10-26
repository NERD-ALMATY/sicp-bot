from sicp_bot.db.models import Cowboy
import jsons


def test_model_encode(cowboy):
    cowboy_bytes_serialized = cowboy.encode()
    cowboy_deserialized = jsons.loadb(cowboy_bytes_serialized, Cowboy)

    assert cowboy_deserialized == cowboy
