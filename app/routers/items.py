import logging
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_item_store
from app.models import Item, ItemCreate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[Item])
async def list_items(
    store: tuple[dict, list] = Depends(get_item_store),
) -> list[Item]:
    items, _ = store
    return [Item(id=k, **v) for k, v in items.items()]


@router.post("/", response_model=Item, status_code=201)
async def create_item(
    body: ItemCreate,
    store: tuple[dict, list] = Depends(get_item_store),
) -> Item:
    items, counter = store
    counter[0] += 1
    item_id = counter[0]
    items[item_id] = {"name": body.name, "description": body.description}
    logger.info("created item id=%d name=%s", item_id, body.name)
    return Item(id=item_id, **items[item_id])


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: int,
    store: tuple[dict, list] = Depends(get_item_store),
) -> Item:
    items, _ = store
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item not found")
    return Item(id=item_id, **items[item_id])


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    store: tuple[dict, list] = Depends(get_item_store),
) -> None:
    items, _ = store
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item not found")
    del items[item_id]
    logger.info("deleted item id=%d", item_id)
