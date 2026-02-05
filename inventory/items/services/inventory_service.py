from items.repo.item_repo import Repo


class InventoryService:
    def __init__(self, _repo:Repo) -> None:
        self._repo = _repo

    def delete_item(self, item_id:int) -> None:
        self._repo.delete(item_id)