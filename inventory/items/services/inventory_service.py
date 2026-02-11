from django.db.models import F
from django.db import transaction, IntegrityError
from items.domain.models import Item


def create_item(name:str, qty:int, user_id) -> Item:
    try:
        with transaction.atomic():
            item = Item(name=name, qty=qty, owner_id=user_id)
            item.save()
            return item

    except IntegrityError:
        raise ValueError("item with that name already exists")


from django.db import transaction

def delete_item(item_id: str, user_id: str) -> None:
    with transaction.atomic():
        deleted_count, _ = Item.objects.filter(id=item_id, owner_id=user_id).delete()

    if deleted_count > 0:
        return

    exists = Item.objects.filter(id=item_id).exists()
    if exists:
        raise PermissionError("forbidden")

    raise ValueError("item not found")



def update_qty(item_id:str, delta:int) -> None:
    if item_id is None:
        return
    
    if isinstance(delta, bool) or not isinstance(delta, int):
        raise ValueError("delta must be an int")

    with transaction.atomic():
        updated = (
            Item.objects
            .filter(id=item_id, qty__gte=-delta)
            .update(qty=F("qty") + delta)
        )

        if updated:
            return Item.objects.get(id=item_id)

        exists = Item.objects.filter(id=item_id).exists()

        if not exists:
            return 

        raise ValueError("qty cannot go below 0")
