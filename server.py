import asyncio
from aiohttp import web
import os
import shutil
import uuid
from collections import defaultdict

routes = web.RouteTableDef()

file_locks = defaultdict(asyncio.Lock)

shutil.rmtree('cache', ignore_errors=True)
os.mkdir('cache')

async def get_slow_data():
    await asyncio.sleep(1)
    return uuid.uuid4().hex

async def cache_file(path):
    with open(path, 'w') as f:
        data = await get_slow_data()
        f.write(data)

@routes.get('/{filename}')
async def get_file(request):
    filename = request.match_info['filename']
    path = f'cache/{filename}'

    async with file_locks[path]:
        if not os.path.exists(path):
            await cache_file(path)

    return web.FileResponse(path)

app = web.Application()
app.add_routes(routes)
web.run_app(
    app,
    host='0.0.0.0',
    port=5000,
)
