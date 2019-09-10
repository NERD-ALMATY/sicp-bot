import re
from copy import deepcopy
from datetime import datetime
from typing import List, Iterator, Type, Optional

from sicp_bot.db.manager import DBManager
from sicp_bot.db.models import Cowboy, Exercise
from sicp_bot.explorer import Explorer, FileDesc, FileTypeEnum
from sicp_bot.parser import ParsePattern

default_cowboy = Cowboy(
    model_id='',
    username='',
    name='',
    repo='',
    last_commit='',
    done=0,
    must_be_done=0,
    created='',
    exercises=[]
)


class Processor:

    def __init__(self, parser: ParsePattern, db_man: DBManager[Cowboy], explorer_cls: Type[Explorer]):
        self._parser = parser
        self._db_man = db_man
        self._explorer_cls = explorer_cls

    def get_leaderboard(self) -> List[Cowboy]:
        self._update_cowboys_exercises()
        return sorted(self.get_cowboys(), key=lambda cowboy: len(cowboy.exercises))[::-1]

    def create_cowboy(self, cowboy: Cowboy) -> Optional[str]:
        assert cowboy.username is not None or cowboy.username != ''
        try:
            self._prevent_duplicate(cowboy)
            cowboy.created = datetime.now().__str__()
            return self._db_man.put(cowboy)
        except AssertionError:
            return None

    def update_cowboy(self, cowboy: Cowboy) -> Optional[str]:
        prev_cowboy = self._db_man.get(cowboy.model_id)
        if prev_cowboy is not None:
            for got_cowboy in self.get_cowboys():
                if got_cowboy.username == cowboy.username and got_cowboy.model_id != prev_cowboy.model_id:
                    raise Exception(f'Cowboy with username: `{cowboy.username}` already exists')
            return self._db_man.update(cowboy)
        else:
            return self.create_cowboy(cowboy)

    def delete_cowboy(self, cowboy_github_nick: str) -> Optional[str]:
        for cowboy in self.get_cowboys():
            if cowboy.username == cowboy_github_nick:
                return self._db_man.delete(cowboy.model_id)
        return None

    def get_cowboy(self, cowboy_github_nick) -> Optional[Cowboy]:
        for cowboy in self.get_cowboys():
            if cowboy.username == cowboy_github_nick:
                return cowboy
        return None

    def get_cowboys(self) -> Iterator[Cowboy]:
        for cowboy in self._db_man.get_models():
            if cowboy is not None:
                yield cowboy

    def _update_cowboys_exercises(self):
        for cowboy in self.get_cowboys():
            explorer = self._explorer_cls(cowboy.username, cowboy.repo)
            if explorer.dir_file_desc is not None and explorer.last_commit != cowboy.last_commit:
                self._tree_matcher(cowboy, explorer.get_dir_tree())
                cowboy.last_commit = explorer.last_commit
                cowboy.must_be_done = _must_be_done(cowboy.created)
                cowboy.done = len(cowboy.exercises)
                self._db_man.update(cowboy)

    def _tree_matcher(self, cowboy: Cowboy, user_tree: FileDesc) -> Cowboy:
        regex = re.compile(self._parser.dir_pattern)
        leaf_files = self._flatten(user_tree)
        cowboy.exercises = []
        for leaf in leaf_files:
            path_str = '/' + '/'.join(leaf.path)
            match = regex.fullmatch(path_str)
            if match is not None and len(match.groups()) > 0:
                ex = Exercise(model_id=path_str)
                cowboy.exercises.append(ex)
        return cowboy

    def _flatten(self, tree: FileDesc) -> List[FileDesc]:
        nodes: List[FileDesc] = []
        for node in tree.children:
            if node.type == FileTypeEnum.FILE:
                nodes.append(node)
            else:
                nodes.extend(self._flatten(node))
        return nodes

    def _prevent_duplicate(self, cowboy: Cowboy) -> None:
        for got_cowboy in self.get_cowboys():
            assert got_cowboy.username != cowboy.username


class Serializer:

    def from_exercises(self, exercises: List[Exercise]) -> str:
        return ', '.join([exercise.model_id for exercise in exercises])

    def from_cowboy_extended(self, cowboy: Cowboy):
        cowboy_str = f'{cowboy.name}: {len(cowboy.exercises)}\n' \
            f'github-repo: [link](https://github.com/{cowboy.username}/{cowboy.repo})\n\n' \
            f'name: {cowboy.name}\n' \
            f'username: {cowboy.username}\n' \
            f'repo: {cowboy.repo}\n' \
            f'last-commit: {cowboy.last_commit[:6]}\n' \
            f'created: {cowboy.created}\n' \
            f'must: {cowboy.must_be_done}\n' \
            f'done: {cowboy.done}\n' \
            f'exercises: \[{self.from_exercises(cowboy.exercises)}\]'
        return cowboy_str

    @staticmethod
    def from_cowboy(cowboy: Cowboy) -> str:
        return f'{cowboy.name}: {cowboy.done}/{cowboy.must_be_done}\n' \
            f'github-repo: [link](https://github.com/{cowboy.username}/{cowboy.repo})'

    @staticmethod
    def leaderboard(cowboys: List[Cowboy]) -> str:
        return '\n\n'.join([Serializer.from_cowboy(cowboy) for cowboy in cowboys])


def _must_be_done(datetime_str: str):
    must_be_done = (datetime.now() - datetime.fromisoformat(datetime_str)).days / 7 * 5
    return 356 if must_be_done >= 356 else int(must_be_done)


class Deserializer:
    cowboy_keys = {
        'username',
        'name',
        'repo',
    }

    def to_cowboy(self, cowboy_str: str) -> Cowboy:
        k_vs = cowboy_str.split('\n')
        cowboy = deepcopy(default_cowboy)
        for k_v in k_vs:
            key, *value = k_v.split(':')
            key = key.strip()
            if key in Deserializer.cowboy_keys:
                setattr(cowboy, key, ''.join(value).strip())
        for key in Deserializer.cowboy_keys:
            assert getattr(cowboy, key) != ''
        return cowboy

    def to_update_cowboy(self, cowboy_str: str, cowboy: Cowboy) -> Cowboy:
        deser_cb = self.to_cowboy(cowboy_str)
        for key in Deserializer.cowboy_keys:
            curr_value = getattr(deser_cb, key)
            if curr_value is not None or curr_value != '':
                setattr(cowboy, key, curr_value)
        return cowboy
