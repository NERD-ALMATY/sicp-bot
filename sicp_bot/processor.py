import re
from copy import copy, deepcopy
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
    exercises=[]
)


class Processor:

    def __init__(self, parser: ParsePattern, db_man: DBManager[Cowboy], explorer_cls: Type[Explorer]):
        self._parser = parser
        self._db_man = db_man
        self._explorer_cls = explorer_cls

    def get_leaderboard(self) -> List[Cowboy]:
        self._update_cowboys_exercises()
        return sorted(self.get_cowboys(), key=lambda cowboy: len(cowboy.exercises))

    def create_cowboy(self, cowboy: Cowboy) -> Optional[str]:
        assert cowboy.username is not None or cowboy.username != ''
        try:
            self._prevent_duplicate(cowboy)
            return self._db_man.put(cowboy)
        except AssertionError:
            return None

    def update_cowboy(self, cowboy: Cowboy) -> Optional[str]:
        prev_cowboy = self._db_man.get(cowboy.model_id)
        if prev_cowboy is not None:
            for got_cowboy in self.get_cowboys():
                if got_cowboy.username == cowboy.username and got_cowboy.model_id != prev_cowboy.model_id:
                    raise Exception('Cowboy with username: `{}` already exists'.format(cowboy.username))
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
            explorer = self._explorer_cls(cowboy.name, cowboy.repo)
            if explorer.dir_file_desc is not None and explorer.last_commit != cowboy.last_commit:
                self._tree_matcher(cowboy, explorer.get_dir_tree())
                cowboy.last_commit = explorer.last_commit
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
            f'exercises: \[{self.from_exercises(cowboy.exercises)}]'
        return cowboy_str

    def from_cowboy(self, cowboy: Cowboy) -> str:
        return f'{cowboy.name}: {len(cowboy.exercises)}\n' \
            f'github-repo: [link](https://github.com/{cowboy.username}/{cowboy.repo})'

    def leaderboard(self, cowboys: List[Cowboy]) -> str:
        return '\n\n'.join([self.from_cowboy(cowboy) for cowboy in cowboys])


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
