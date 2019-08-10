from dataclasses import dataclass
from typing import List
from src.db import BaseModel


@dataclass
class Exercise(BaseModel):
    par_id: str
    sub_id: str
    mandatory: bool
    done: bool


@dataclass
class Cowboy(BaseModel):
    name: str
    tgname: str
    username: str
    repo: str
    last_commit: str
    exercises: List[Exercise]
