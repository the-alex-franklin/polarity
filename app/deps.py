from collections.abc import Generator

# In-memory store standing in for a real database.
# Replace with a real DB session in a real app.
_items: dict[int, dict] = {}
_counter: list[int] = [0]


def get_item_store() -> Generator[tuple[dict[int, dict], list[int]], None, None]:
    yield _items, _counter
