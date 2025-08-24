import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from api.app import app  # ensure package path matches your layout

@pytest.mark.asyncio
async def test_healthz():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/healthz")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "build" in data

@pytest.mark.asyncio
async def test_echo_default():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/echo")
        assert r.status_code == 200
        assert r.json()["msg"] == "hi"

@pytest.mark.asyncio
async def test_echo_param():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/echo", params={"msg": "wolf"})
        assert r.status_code == 200
        assert r.json()["msg"] == "wolf"
