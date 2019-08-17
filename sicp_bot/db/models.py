from dataclasses import dataclass
from typing import List
from sicp_bot.db import BaseModel


@dataclass
class Exercise(BaseModel):
    pass

@dataclass
class Cowboy(BaseModel):
    name: str
    username: str
    repo: str
    last_commit: str
    exercises: List[Exercise]
