from dataclasses import dataclass

@dataclass(frozen=True)
class ItemModel:
    id: str
    name: str
    qty: int