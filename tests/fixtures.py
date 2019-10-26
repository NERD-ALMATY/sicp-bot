from typing import Dict, List

import pytest

from db.models import Exercise, Cowboy
from tests.factories import ExerciseFactory


@pytest.fixture()
def mock_config_dict() -> Dict[str, str]:
    return {
        "CERT": "1",
        "DEBUG": "2",
        "DIR_PATTERN": "3",
        "GITHUB_TOKEN": "4",
        "HOST": "5",
        "ISSUER_ID": "6",
        "KEY": "7",
        "LISTEN": "8",
        "PORT": "9",
        "TELE_TOKEN": "0",
    }


@pytest.fixture()
def exercise() -> Exercise:
    return ExerciseFactory.exercise("0")


@pytest.fixture()
def exercises() -> List[Exercise]:
    return ExerciseFactory.exercises(10)


@pytest.fixture()
def cowboy(exercises: List[Exercise]) -> Cowboy:
    pass
