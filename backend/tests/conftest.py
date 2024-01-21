import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from typing import AsyncGenerator
import pytest
from quart import Quart
from backend.run import app


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    async with app.test_app():
        yield app