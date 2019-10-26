from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from github import Github
from github.Repository import Repository

from .logger import get_logger

_g: Optional[Github] = None
logger = get_logger(__name__)


class Explorer:
    def __init__(self, user: str, repo_name: str):
        assert isinstance(_g, Github)
        self.dir_file_desc: Optional[FileDesc] = None
        try:
            self.user_repo: Repository = _g.get_user(user).get_repo(repo_name)
            self.dir_file_desc = FileDesc(
                name="/", type=FileTypeEnum.DIR, path=[], children=[]
            )
            self.last_commit = self._get_last_commit()
        except Exception as e:
            logger.info(
                f"Couldn't find a repo for cowboy a : {user}/{repo_name}",
                exc_info=e,
            )

    def get_dir_tree(self) -> FileDesc:
        if self.dir_file_desc is None:
            raise ValueError("Repository is not available")
        self.dir_file_desc.children = self._traverse(self.dir_file_desc)
        return self.dir_file_desc

    def _traverse(self, file_desc: FileDesc) -> List[FileDesc]:
        file_desc_children = []
        cur_path = "/".join(file_desc.path) if file_desc.path != ["/"] else "/"
        for content in self.user_repo.get_dir_contents(cur_path):
            if content.type != "dir":
                cur_file = FileDesc(
                    name=content.name,
                    type=_content_type_to_file_type(content.type),
                    path=[*file_desc.path, content.name],
                    children=[],
                )
                file_desc_children.append(cur_file)
            else:
                cur_dir = FileDesc(
                    name=content.name,
                    type=_content_type_to_file_type(content.type),
                    path=[*file_desc.path, content.name],
                    children=[],
                )
                cur_dir.children.extend(self._traverse(cur_dir))

                file_desc_children.append(cur_dir)

        return file_desc_children

    def _get_last_commit(self):
        return self.user_repo.get_commits()[0].commit.sha


class FileTypeEnum(Enum):
    DIR = 0
    FILE = 1


@dataclass
class FileDesc:
    name: str
    type: FileTypeEnum
    path: List[str]
    children: List[FileDesc]


_g_to_f_map = {"dir": FileTypeEnum.DIR, "file": FileTypeEnum.FILE}


def _content_type_to_file_type(content_type):
    return _g_to_f_map[content_type]


def get_explorer_cls(api_token=None):
    global _g
    _g = Github(login_or_token=api_token)
    return Explorer
