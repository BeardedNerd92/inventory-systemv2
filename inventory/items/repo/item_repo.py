from __future__ import annotations
from items.domain.models import ItemModel
from typing import Dict, Optional
import uuid

class Repo:
    def __init__(self) -> None:
        self._by_id: Dict[str, ItemModel] = {}

    
    def create(self, name: str, qty: int) -> ItemModel:
        item_id = str(uuid.uuid4()) 
        item = ItemModel(id=item_id, name=name, qty=qty)
        self._by_id[item_id] = item
        return item
    
    def get(self, item_id:str) -> Optional[ItemModel]: 
        return self._by_id.get(item_id)
    
    def list(self) -> Dict[str, ItemModel]:
        return dict(self._by_id)
    
    def delete(self, item_id:str) -> bool:
        return self._by_id.pop(item_id, None) is not None