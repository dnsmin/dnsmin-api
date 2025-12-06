from pydantic import BaseModel as PydanticBaseModel
from typing import List


class ValueHashMixIn:

    @property
    def _hash_keys(self) -> List[str]:
        return []

    @property
    def value_hash(self) -> str:
        """Generates a hash for this model's values based on the configured hash keys."""
        import hashlib, json

        if not self._hash_keys:
            raise ValueError('The model does not define any hash keys.')

        data = {
            key: getattr(self, key)
            for key in self._hash_keys
            if hasattr(self, key)
        }

        json_bytes = json.dumps(data, sort_keys=True, default=str).encode('utf-8')

        return hashlib.sha256(json_bytes).hexdigest()

    @staticmethod
    def drop_matches(queue, map1, map2, modify_in_place: bool = False) -> list[str]:
        final = queue.copy() if not modify_in_place else queue
        for name in queue.copy():
            if map1[name].value_hash == map2[name].value_hash:
                final.remove(name)
        return final


class BaseModel(ValueHashMixIn, PydanticBaseModel):
    """This provides an abstract base class for all app models to inherit from."""


from .api import *
from .db import *
