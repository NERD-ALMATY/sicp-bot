from typing import List

from sicp_bot.db.models import Exercise


class ExerciseFactory:
    @classmethod
    def exercise(cls, model_id: str) -> Exercise:
        return Exercise(model_id)

    @classmethod
    def exercises(cls, count: int = 10) -> List[Exercise]:
        return [Exercise(str(i)) for i in range(count)]


class CowboyFactory:
    @classmethod
    def cowboy(cls, **kwargs):

        (ExerciseFactory.exercises(),)
