from pytest import mark
from quart import Quart
from typing import AsyncGenerator

@mark.asyncio
async def test_control(app: AsyncGenerator[Quart, None]):
    async for a in app:
        async with a.test_client() as test_client:
            response = await test_client.get("/control/ping/")
            assert (await response.get_json())["ping"] == "pong"