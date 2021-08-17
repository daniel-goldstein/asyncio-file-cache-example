from aiohttp import web
import os
import shutil
import uuid

routes = web.RouteTableDef()

shutil.rmtree('cache', ignore_errors=True)
os.mkdir('cache')

def cache_file(path):
    with open(path, 'w') as f:
        f.write(uuid.uuid4().hex)

@routes.get('/{filename}')
async def get_file(request):
    filename = request.match_info['filename']
    path = f'cache/{filename}'

    if not os.path.exists(path):
        cache_file(path)

    return web.FileResponse(path)

app = web.Application()
app.add_routes(routes)
web.run_app(
    app,
    host='0.0.0.0',
    port=5000,
)
