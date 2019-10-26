from __future__ import annotations

from typing import List, Iterator, Optional, Type, TypeVar, Generic
import uuid
import plyvel as pv
import jsons
from ..db import BaseModel


class _KeysType(List[str]):
    def __init__(self, list_name: str, db: pv.DB):
        assert list_name is not None and isinstance(db, pv.DB)
        self._list_name = list_name.encode()
        self._db = db
        keys: bytes = self._db.get(self._list_name)
        if keys is not None:
            super().__init__(list(jsons.loadb(keys)))
        else:
            super().__init__()

    def _rewrite_db(self):
        self._db.put(self._list_name, jsons.dumpb(self))

    def append(self, key: str):
        if key not in self:
            super(_KeysType, self).append(key)
            self._rewrite_db()

    def remove(self, key: str):
        if key in self:
            super(_KeysType, self).remove(key)
            self._rewrite_db()


ModelTV = TypeVar("ModelTV", bound=BaseModel)


class DBManager(Generic[ModelTV]):
    def __init__(
        self, path: str, object_type: Type[ModelTV], create_if_missing=True
    ):
        self._db: pv.DB = pv.DB(path, create_if_missing=create_if_missing)
        self._object_type = object_type
        self._list_name = f"keys_{self._object_type}"
        self._keys: _KeysType = _KeysType(
            list_name=self._list_name, db=self._db
        )

    def _is_valid_model(self, model: ModelTV):
        assert isinstance(model, self._object_type)

    def put(self, model: ModelTV) -> str:
        self._is_valid_model(model)
        model.model_id = uuid.uuid4().hex
        self._db.put(model.model_id.encode(), model.encode())
        self._keys.append(model.model_id)
        return model.model_id

    def update(self, model: ModelTV) -> str:
        self.delete(model.model_id)
        return self.put(model)

    def delete(self, model_id: str):
        self._db.delete(model_id.encode())
        self._keys.remove(model_id)
        return model_id

    def get(self, model_id: str) -> Optional[ModelTV]:
        if model_id.encode() in self._keys:
            return None
        return self._decode(self._db.get(model_id.encode()))

    def get_model_ids(self) -> Iterator[str]:
        for key in self._keys:
            yield key

    def get_models(self) -> Iterator[Optional[ModelTV]]:
        for model in map(
            lambda model_id: self.get(model_id), self.get_model_ids()
        ):
            yield model

    def _decode(self, byte_object: bytes) -> ModelTV:
        return jsons.loadb(byte_object, self._object_type)
