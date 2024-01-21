from typing import AsyncGenerator
import pytest
from quart import Quart
from src.backend.run import app


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    async with app.test_app():
        yield app