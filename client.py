import aiohttp
import asyncio
import random
import uuid

fnames = [
    'file_' + uuid.uuid4().hex[:5]
    for _ in range(10)
]

async def read_file(session, fname):
    resp = await session.get(
        f'http://localhost:5000/{fname}'
    )
    content = await resp.text()
    assert content

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(
            read_file(session, random.choice(fnames))
            for _ in range(10_000)
        ))

asyncio.get_event_loop().run_until_complete(main())
