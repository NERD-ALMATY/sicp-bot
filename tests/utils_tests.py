from pathlib import Path

from sicp_bot import get_data_folder_path


# TODO: patch it properly
def test_get_data_folder_path():
    assert get_data_folder_path() == f"{Path(__file__).parent.parent}/data/"
