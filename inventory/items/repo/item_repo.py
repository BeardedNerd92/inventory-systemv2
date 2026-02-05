from __future__ import annotations
from items.domain.models import ItemModel
from typing import Dict, Optional

class Repo:
    def __init__(self) -> None:
        self._by_id: Dict[int, ItemModel] = {}
        self._next_id = 1
    
    def create(self, name: str, qty: int) -> ItemModel:
        item = ItemModel(id=self._next_id, name=name, qty=qty)
        self._by_id[item.id] = item
        self._next_id += 1
        return item
    
    def get(self, item_id:int) -> Optional[None]:
        return self._by_id.get(item_id)
    
    def delete(self, item_id:int) -> bool:
        return self._by_id.pop(item_id, None) is not None