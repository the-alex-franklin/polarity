import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(autouse=True)
def reset_store():
    from app.deps import _items, _counter
    _items.clear()
    _counter[0] = 0


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_and_get_item(client: AsyncClient):
    r = await client.post("/items/", json={"name": "widget", "description": "a thing"})
    assert r.status_code == 201
    item = r.json()
    assert item["name"] == "widget"
    assert item["id"] == 1

    r2 = await client.get(f"/items/{item['id']}")
    assert r2.status_code == 200
    assert r2.json() == item


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient):
    await client.post("/items/", json={"name": "a"})
    await client.post("/items/", json={"name": "b"})
    r = await client.get("/items/")
    assert r.status_code == 200
    assert len(r.json()) == 2


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    r = await client.post("/items/", json={"name": "bye"})
    item_id = r.json()["id"]
    r2 = await client.delete(f"/items/{item_id}")
    assert r2.status_code == 204
    r3 = await client.get(f"/items/{item_id}")
    assert r3.status_code == 404


@pytest.mark.asyncio
async def test_blank_name_rejected(client: AsyncClient):
    r = await client.post("/items/", json={"name": "   "})
    assert r.status_code == 422
