from dataclasses import dataclass

import jsons


@dataclass
class BaseModel(object):

    model_id: str

    def encode(self):
        return jsons.dumpb(self)
