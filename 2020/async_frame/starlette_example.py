# coding:utf-8
__doc__ = """
看starlette是如何封装uvicorn.
"""

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})


routes = [
    Route("/", endpoint=homepage)
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run("starlette_example:app", host="127.0.0.1", port=7000, log_level="info")
